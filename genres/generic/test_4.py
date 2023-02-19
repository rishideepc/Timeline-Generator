# import sqlite3
# from nltk.stem import WordNetLemmatizer, PorterStemmer
# import nltk
# # nltk.download('wordnet')
# connect_=sqlite3.connect('timeline-data.db')
# keyword='India'
# cursor_=connect_.cursor()

# cursor_.execute(f'''

# SELECT * FROM Disaster

# ''')


# # WHERE location LIKE '{keyword}'
# # print(cursor_.fetchall())
# items = cursor_.fetchall()
# titles=[]
# # print(items)
# for index,item in enumerate(items):
# #     print(f'''
# #     {index+1}
# #     Title: {item[0]}
# #     DateTime: {item[1]}
# #     Type: {item[2]}
# #     Location: {item[3]}
# #     Casualty Count: {item[4]}
# #     Severity: {item[5]}
# #     CronJobDate: {item[6]}
# #     ''')
#     titles.append(item[0])

# ################# Lemmatization / Tokenization Test Script ###################
# sentence_1="death dead died deadly die dies dying"
# sentence_2='fear feared fearing fears'
# sentence_3='injured injure injury'
# sentence_4='kill kills killed killing'
# sentence_5='buries buried bury burying burial'
# sentence_6='hit hits'
# sentence_7='trap trapped trapping'
# sentence_8='threat threaten threatening threatens threatened'
# sentence_9='hurt hurting hurts'

# word_list= nltk.word_tokenize(sentence_9)
# print(word_list)
# print('\n')
# print('Lemmatized Output:')
# lemmatizer=WordNetLemmatizer()
# lemmatized_output= ' '.join([lemmatizer.lemmatize(w) for w in word_list])
# print(lemmatized_output)
# print('\n')
# print('Stemmed Output: ')
# ps= PorterStemmer()
# stemmed_output= ' '.join([ps.stem(w) for w in word_list])
# print(stemmed_output)
    

# connect_.commit()
# connect_.close()
# from word2number import w2n
# def has_number_words(sentence):
#     words= sentence.split()

#     for word in words:
#         try:
#             num = w2n.word_to_num(word)
#             return True, num
#         except ValueError:
#             continue
#     return False

# if __name__=="__main__":
#     has_number_words("Five has grown.")


from ast import keyword
from xmlrpc.client import DateTime
import requests
from bs4 import BeautifulSoup
import urllib, json
import time
from datetime import *
import re
############################################################
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
############################################################
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.metrics import accuracy_score
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
import re
import sqlite3
from word2number import w2n
from PIL import Image
from pygooglenews import GoogleNews


today= date.today()
cron_job_date_=f'{today.strftime("%b-%d-%Y")}'
def fetch_gnews_article(keyword):
    connect_=sqlite3.connect('timeline-data.db')
    cursor_=connect_.cursor()
    gn= GoogleNews()
    articles= gn.search(f'{keyword}')
    for article in articles['entries']:
        title=article.get('title')
        link=article.get('link')
        html=requests.get(url=link)
        soup=BeautifulSoup(html.content, 'lxml')
        paragraphs= soup.find_all('p', text=True)
        type_=keyword
        location="none"
        casualty_injured="none"
        tokenized_text= word_tokenize(paragraph)
        classified_text= st.tag(tokenized_text)
        for word, tag in classified_text:
            if tag=="LOCATION":
                location=word

        ps= PorterStemmer()
        stemmed_output=' '.join([ps.stem(t) for t in tokenized_text])
        temp=re.compile(r'die|death|dead|deadli|kill|buri').search(stemmed_output)
        if not temp:
            temp_2=re.compile(r'injuri|injur|hit|trap|fear|threat|threaten|hurt').search(stemmed_output)
            if not temp_2:
                casualty_injured="Casualty not found"
            else:
                temp_3=re.compile(r' \d\d\d | \d\d | \d ').search(stemmed_output)
                if not temp_3:
                    casualty_injured= "Casualty found - Couldn't detect count of injured."
                else:
                        casualty_injured= f"Injuries: {temp_3.group()}"
        else:
            temp_1=re.compile(r' \d\d\d | \d\d | \d ').search(stemmed_output)
            if not temp_1:
                if has_number_words(title) == False:
                    casualty_injured= "Casualty Found - Couldn't detect count of casualities."
                
                else:
                    _, casualty_value= has_number_words(title)
                    casualty_injured= f"Casualties: {casualty_value}"
            else:
                casualty_injured= f"Casualties: {temp_1.group()}"

        severity_label=severity_model(title=title)
        set_=(title.lower(), type_.lower(), location.lower(), casualty_injured, severity_label[0].lower(), cron_job_date_)
        cursor_.execute("INSERT INTO Disaster values(?, ?, ?, ?, ?, ?)", set_)
        print(f'''
            {index+1}.  Title: {title.lower()}
                Event Date-time: {date_}
                Event Type: {type_.lower()}
                Location: {location.lower()}
                Casualty/Injured: {casualty_injured}
                Severity: {severity_label[0].lower()}
                            \n
        ''')

        print("\n\n")



