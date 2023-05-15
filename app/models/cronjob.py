import sys
import requests
from bs4 import BeautifulSoup
from datetime import *
from nltk.tag import StanfordNERTagger
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
from word2number import w2n
from pygooglenews import GoogleNews
import pickle
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from app.models.dao import DAOOperations
from app.models.severity import vectorized
from app.models.bert_qa import BertQA


class CronJob:
    def __init__(self):
        self.st = StanfordNERTagger(
            '..\\resources\\stanford-ner-2020-11-17\\classifiers\\english.all.3class.distsim.crf.ser.gz',
            '..\\resources\\stanford-ner-2020-11-17\\stanford-ner.jar',
            encoding='utf-8')
        self.keywords_disaster = ['landslide']
        self.gn = GoogleNews()
        self.dao = DAOOperations()
        self.bert = BertQA()
        self.endpoint = "http://api.positionstack.com/v1/forward"
        self.access_key = "2e9fd33a8efefbcd7fa0181c9cde822c"

    # def __del__(self):
    #     del self.dao

    def has_number_words(self, sentence):
        words = sentence.split()

        for word in words:
            try:
                num = w2n.word_to_num(word)
                return True, num
            except ValueError:
                continue
        return False

    def get_articles(self, keyword):
        return self.gn.search(f'{keyword}')

    def get_details(self, article):
        title = article.get('title')
        link = article.get('link')
        pubdate = article.get('published')
        html = requests.get(url=link)
        soup = BeautifulSoup(html.content, 'lxml')
        paragraphs = soup.find_all('p', text=True)
        content = '\n'.join([para.string for para in paragraphs])
        content = content.strip()
        return title, link, pubdate, content

    def get_location(self, title, content):
        tokenized_text = word_tokenize(title)
        classified_text = self.st.tag(tokenized_text)
        location = ""
        for word, tag in classified_text:
            if tag == "LOCATION":
                location = word

        if not location:
            tokenized_text_ = word_tokenize(content)
            classified_text_ = self.st.tag(tokenized_text_)
            for word, tag in classified_text_:
                if tag == "LOCATION":
                    location = word
        return location

    def get_severity(self, content):
        pickled_model_gini = pickle.load(open('..\\resources\\severity_model.pkl', 'rb'))
        X_test = pd.Series(content)
        xv_test = vectorized.transform(X_test)
        severity_label = pickled_model_gini.predict(xv_test)
        return severity_label

    def get_text_summary(self, content):
        parser = PlaintextParser.from_string(content, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 1)
        text_summary = ""

        for sentence in summary:
            text_summary += str(sentence)

        return text_summary

    def get_casualty(self, title, content):
        tokenized_text = word_tokenize(title)
        tokenized_text_ = word_tokenize(content)
        flag = 1
        ps = PorterStemmer()
        stemmed_output = ' '.join([ps.stem(t) for t in tokenized_text])
        temp = re.compile(r'die|death|dead|deadli|kill|buri').search(stemmed_output)
        if not temp:
            temp_2 = re.compile(r'injuri|injur|hit|trap|fear|threat|threaten|hurt').search(stemmed_output)
            if not temp_2:
                casualty_injured = "Casualty or injury not found"
                flag = 0
            else:
                temp_3 = re.compile(r' \d\d\d | \d\d | \d ').search(stemmed_output)
                if not temp_3:
                    if not self.has_number_words(title):
                        casualty_injured = "Injury found - Couldn't detect count of injured."
                    else:
                        _, casualty_value = self.has_number_words(title)
                        casualty_injured = f"Injuries: {casualty_value}"
                else:
                    casualty_injured = f"Injuries: {temp_3.group()}"
        else:
            temp_1 = re.compile(r' \d\d\d | \d\d | \d ').search(stemmed_output)
            if not temp_1:
                if not self.has_number_words(title):
                    casualty_injured = "Casualty Found - Couldn't detect count of casualities."
                else:
                    _, casualty_value = self.has_number_words(title)
                    casualty_injured = f"Casualties: {casualty_value}"
            else:
                casualty_injured = f"Casualties: {temp_1.group()}"

        if not flag:
            ps_ = PorterStemmer()
            stemmed_output_ = ' '.join([ps_.stem(t) for t in tokenized_text_])
            temp = re.compile(r'die|death|dead|deadli|kill|buri').search(stemmed_output_)
            if not temp:
                temp_2 = re.compile(r'injuri|injur|hit|trap|fear|threat|threaten|hurt').search(stemmed_output_)
                if not temp_2:
                    casualty_injured = "Casualty or injury not found"
                else:
                    temp_3 = re.compile(r' \d\d\d | \d\d | \d ').search(stemmed_output_)
                    if not temp_3:
                        if not self.has_number_words(content):
                            casualty_injured = "Injuries Found - Couldn't detect count of casualities."
                        else:
                            _, casualty_value = self.has_number_words(content)
                            casualty_injured = f"Injuries: {casualty_value}"
                    else:
                        casualty_injured = f"Injuries: {temp_3.group()}"
            else:
                temp_1 = re.compile(r' \d\d\d | \d\d | \d ').search(stemmed_output_)
                if not temp_1:
                    if not self.has_number_words(content):
                        casualty_injured = "Casualty Found - Couldn't detect count of casualities."
                    else:
                        _, casualty_value = self.has_number_words(content)
                        casualty_injured = f"Casualties: {casualty_value}"
                else:
                    casualty_injured = f"Casualties: {temp_1.group()}"
        return casualty_injured

    def combine_results(self, bert_results, location, casualty_injured):
        date_ = bert_results[2]
        loc = bert_results[3]
        if loc != "Negative" and not location:
            location = loc
        if casualty_injured == "Casualty or injury not found":
            if bert_results[4] != "Negative":
                casualty_injured = f"Casualty: {bert_results[4]}"
            if bert_results[5] != "Negative":
                if "not found" in casualty_injured:
                    casualty_injured = f"Injuries : {bert_results[5]}"
                else:
                    casualty_injured += f"Injuries : {bert_results[5]}"
            if bert_results[6] != "Negative":
                if "not found" in casualty_injured:
                    casualty_injured = f"Affected : {bert_results[6]}"
                else:
                    casualty_injured += f"Affected : {bert_results[6]}"
        params_2 = {
            'access_key': self.access_key,
            'query': location,
            'limit': 1
        }
        response = requests.get(self.endpoint, params=params_2).json()
        latitude, longitude = response['data'][0]['latitude'], response['data'][0]['longitude']
        return date_, location, casualty_injured, latitude, longitude

    def fetch_gnews_article(self):
        keyword = self.keywords_disaster[0]
        today = date.today()
        cron_job_date_ = f'{today.strftime("%b-%d-%Y")}'
        articles = self.get_articles(keyword)
        for index, article in enumerate(articles['entries']):
            if index >= 100:
                break
            try:
                title, link, pubdate, content = self.get_details(article)
                type_ = keyword
                bert_details = self.bert.wrapper(content)
                location = self.get_location(title, content)
                severity_label = self.get_severity(content)
                text_summary = self.get_text_summary(content)
                casualty_injured = self.get_casualty(title, content)
                date_, location, casualty_injured, latitude, longitude \
                    = self.combine_results(bert_details, location, casualty_injured)
                self.dao.insert(title, content, type_, location, casualty_injured, severity_label, text_summary,
                                cron_job_date_, date_, latitude, longitude)
            except Exception:
                pass
        self.dao.connect_.close()


if __name__ == "__main__":
    obj = CronJob()
    obj.fetch_gnews_article()