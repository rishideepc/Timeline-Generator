from ast import keyword
from xmlrpc.client import DateTime
import requests
from bs4 import BeautifulSoup
import urllib, json
import time
from datetime import *
import re
##########################################################
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
# import seaborn as sns
import re
import sqlite3
from word2number import w2n
from PIL import Image
from pygooglenews import GoogleNews
import pickle
###########################################################

# Initialization script
st = StanfordNERTagger('C:\\Users\\HP\\Desktop\\Python_AI\\Timeline_Generator\\timeline\\templates\\stanford-ner-2020-11-17\\classifiers\\english.all.3class.distsim.crf.ser.gz',
					   'C:\\Users\\HP\\Desktop\\Python_AI\\Timeline_Generator\\timeline\\templates\\stanford-ner-2020-11-17\\stanford-ner.jar',
					   encoding='utf-8')

# Keywords for Disaster Class
# keywords_disaster=['landslide', 'earthquake', 'tsunami', 'flood']
keywords_disaster= ['landslide']


####################### ****** NEWS SCRAPPER CLASS ********** ##################################
# class NewsScrapper(keyword):
#     def __init__(self):
#         gn= GoogleNews()
#         self.keyword= gn.search(f'india+{keyword}')

#     def get_content_metadata(self, article):
#         title= article.get('title')
#         link= article.get('link')
#         return title, link

#     def save_image(self, article_number, images):
#         image_number=1
#         alt_map={}
#         for image in images:
#             image_url, alt= get_image_details(image)
#             alt_map[image_number]= alt

#     ################################################################################
#     def get_content(self, article_number, paragraphs, title, link):
#         content = '\n'.join([para.string for para in paragraphs])
#         content = content.strip()
#         if not content:
#             print('Empty')

#         return content

#     def get_html(self, link):
#         try:
#             html= requests.get(url= link)

#         except:
#             raise Exception(f'error in get call to url {link}')

#         return html

#     def soup_operations(self, html):
#         soup= BeautifulSoup(html.content, 'lxml')
#         paragraphs= soup.findAll('p', text=True)
#         return paragraphs

#     def driver():
#         article_number=1
#         for article in self.keyword['entries']:
#             try:
#                 title, link= self.get_content_metadata(article)
#                 type_=keyword
#                 html= self.get_html(link)
#                 paragraphs= self.soup_operations(html)

#                 self.get_content(article_number, paragraphs, title, link)
#                 article_number+=1
#             except:
#                 print('Error')
        

#################################################################################################

######################## ************ CHECKING STRING NUMERICALS *************** ####################
def has_number_words(sentence):
    words= sentence.split()

    for word in words:
        try:
            num = w2n.word_to_num(word)
            return True, num
        except ValueError:
            continue
    return False
########################## ***************************************** ########################

# ################################################################################################
# def prediction(X_test, model_object):
#     y_pred= model_object.predict(xv_test)
#     # print("Predicted values: ")
#     return y_pre
# ################################################################################################


#################################################################################################################################

##############################################################################################################################



##############################*********************CRON JOB SCRIPT*********************#######################################################
today= date.today()
cron_job_date_=f'{today.strftime("%b-%d-%Y")}'
def fetch_gnews_article(keyword):
    connect_=sqlite3.connect('timeline-data.db')
    cursor_=connect_.cursor()
    gn= GoogleNews()
    articles= gn.search(f'{keyword}')
    for index, article in enumerate(articles['entries']):
        if index<10:
            title=article.get('title')
            link=article.get('link')
            pubdate=article.get('published')
            print("PUBLISHED DATE: ", pubdate)
            html=requests.get(url=link)
            soup=BeautifulSoup(html.content, 'lxml')
            paragraphs= soup.find_all('p', text=True)
            content = '\n'.join([para.string for para in paragraphs])
            content = content.strip()
            type_=keyword
            location="none"
            casualty_injured="none"
            tokenized_text= word_tokenize(title)
            classified_text= st.tag(tokenized_text)
            for word, tag in classified_text:
                if tag=="LOCATION":
                    location=word

                if location=="none":
                    tokenized_text= word_tokenize(content)
                    classified_text= st.tag(tokenized_text)
                    for word, tag in classified_text:
                        if tag=="LOCATION":
                            location=word
            flag=1
            ps= PorterStemmer()
            stemmed_output=' '.join([ps.stem(t) for t in title])
            temp=re.compile(r'die|death|dead|deadli|kill|buri').search(stemmed_output)
            if not temp:
                temp_2=re.compile(r'injuri|injur|hit|trap|fear|threat|threaten|hurt').search(stemmed_output)
                if not temp_2:
                    casualty_injured="Casualty or injury not found"
                    flag=0

                else:
                    temp_3=re.compile(r' \d\d\d | \d\d | \d ').search(stemmed_output)
                    if not temp_3:
                        casualty_injured= "Injury found - Couldn't detect count of injured."
                        # flag=0
                    else:
                        casualty_injured= f"Injuries: {temp_3.group()}"
            else:
                temp_1=re.compile(r' \d\d\d | \d\d | \d ').search(stemmed_output)
                if not temp_1:
                    if has_number_words(title) == False:
                        casualty_injured= "Casualty Found - Couldn't detect count of casualities."
                        # flag=0
                    
                    else:
                        _, casualty_value= has_number_words(title)
                        casualty_injured= f"Casualties: {casualty_value}"
                else:
                    casualty_injured= f"Casualties: {temp_1.group()}"

            if(flag==0):
                ps_= PorterStemmer()
                stemmed_output_=' '.join([ps_.stem(t) for t in content])
                temp=re.compile(r'die|death|dead|deadli|kill|buri').search(stemmed_output_)
                if not temp:
                    temp_2=re.compile(r'injuri|injur|hit|trap|fear|threat|threaten|hurt').search(stemmed_output_)
                    if not temp_2:
                        casualty_injured="Casualty or injury not found+"
                        flag=1

                    else:
                        temp_3=re.compile(r' \d\d\d | \d\d | \d ').search(stemmed_output_)
                        if not temp_3:
                            casualty_injured= "Injury found - Couldn't detect count of injured.+"
                            flag=1
                        else:
                            casualty_injured= f"Injuries: {temp_3.group()}+"
                            flag=1
                else:
                    temp_1=re.compile(r' \d\d\d | \d\d | \d ').search(stemmed_output_)
                    if not temp_1:
                        if has_number_words(content) == False:
                            casualty_injured= "Casualty Found - Couldn't detect count of casualities.+"
                            flag=1

                        else:
                            _, casualty_value= has_number_words(content)
                            casualty_injured= f"Casualties: {casualty_value}+"
                            flag=1
                    else:
                        casualty_injured= f"Casualties: {temp_1.group()}+"
                        flag=1

            ####################################################
            # severity_label=severity_model(title=content)
            # pickled_model_gini = pickle.load(open('C:/Users/HP/Desktop/Python_AI/Timeline_Generator/genres/generic/severity_label/severity_model.pkl', 'rb'))
            pickled_model_gini = pickle.load(open('severity_model.pkl', 'rb'))
            X_test= pd.Series(content)
            from severity_label.model import vectorized
            xv_test= vectorized.transform(X_test)
            severity_label= pickled_model_gini.predict(xv_test)
            ####################################################
            set_=(title.lower(), content.lower(), type_.lower(), location.lower(), casualty_injured, severity_label[0].lower(), cron_job_date_)
            cursor_.execute("INSERT INTO Landslide values(?, ?, ?, ?, ?, ?, ?)", set_)
            print(f'''
                {index+1}.  Title: {title.lower()}
                    Paragraph: {content.lower()}
                    Event Type: {type_.lower()}
                    Location: {location.lower()}
                    Casualty/Injured: {casualty_injured}
                    Severity: {severity_label[0].lower()}
                    Cron_Job Date: {cron_job_date_}
                                \n
            ''')

            print("\n\n")

###############################################################################################

        # for i in range(1, 101):
        #     if i!=100:
        #         for j in range(i+1, 101):
        #             x=db.child(f'{today.strftime("%b-%d-%Y")}').child('Disaster-Data').child(f'News Feature-{keywords[i]}').child(f'News Item-{j}').child('Location').get().val()
        #             db.child(f'{today.strftime("%b-%d-%Y")}').child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(f'News Item-{i}').order_by_key().order_by_child('Location').equal_to(x).remove()
        #             break

        # for i in range(1, 100):
        #     if i!=99:
        #         for j in range(i+1, 101):
        #             db.child(f'{today.strftime("%b-%d-%Y")}').child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(f'News Item-{i}').order_by_key().order_by_child('Location').equal_to(arr_[j]).remove()
                    
        #             break


            
        # def Remove(duplicate):
        #     final_list = []
        #     for num in duplicate:
        #         if num not in final_list:
        #             final_list.append(num)
        #         return final_list

#########################################################################
#     cursor_.execute('''

# SELECT * FROM Disaster

# ''')
#     items=cursor_.fetchall()
#     len_=len(items)
#     for i in range(0, len_):
#         if i!=len_-1:
#             for j in range(i+1, len_):
#                 if(items[j][1]==items[i][1]):
#                     items[i][1]="null"

#         else:
#             break


    connect_.commit()
    connect_.close()

if __name__=="__main__":

    ########################################  **FUNCTION CALL**   ################################
    fetch_gnews_article(keywords_disaster[0])
    ######################################## ---X-------X------  ################################


#########################################********CRON JOB ENDS*************##############################