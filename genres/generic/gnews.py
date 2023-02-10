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
###########################################################

# Initialization script
st = StanfordNERTagger('C:\\Users\\HP\\Desktop\\Python_AI\\Timeline_Generator\\timeline\\templates\\stanford-ner-2020-11-17\\classifiers\\english.all.3class.distsim.crf.ser.gz',
					   'C:\\Users\\HP\\Desktop\\Python_AI\\Timeline_Generator\\timeline\\templates\\stanford-ner-2020-11-17\\stanford-ner.jar',
					   encoding='utf-8')

# Keywords for Disaster Class
# keywords_disaster=['landslide', 'earthquake', 'tsunami', 'flood']
keywords_disaster= ['landslide']


############## ******************TRAINING THE SEVERITY MODEL*********************** #########################
def severity_model(title):
    data= pd.read_excel('C:/Users/HP/Desktop/Python_AI/Timeline_Generator/genres/generic/severity_label/Labelled.xlsx')

    ################################ Data cleansing ##################################
    for j in range(0, 596):
        data['Label'][j]=data['Label'][j].lower()
        data['Label'][j]=re.sub(" ", "", data['Label'][j])
        data['News-Item'][j]=re.sub('https?://\S+|www\.\S+', '', data['News-Item'][j])
        data['News-Item'][j]=re.sub('\[.*?\]', '', data['News-Item'][j])
        data['News-Item'][j]=re.sub('<.*?>+', '', data['News-Item'][j])
        data['News-Item'][j]=re.sub('\w*\d\w*', '', data['News-Item'][j])  
    ############################### XXXXXXXXXXXXXXXX ################################
    X_train= data['News-Item']  # Feature Column
    y_train= data['Label']  # Target Colum
     ###################### Vectorization && Transformation ####################################
    vectorization= TfidfVectorizer()
    xv_train= vectorization.fit_transform(X_train)
    ##################### XXXXXXXXXXXXXXXXXXXXXXXXXX ################################

    ###################### Training #################################################
    # model_gini= DecisionTreeClassifier(criterion="gini", random_state=123, max_depth=10, min_samples_leaf=6)
    model_gini=svm.SVC(kernel='linear')
    model_gini.fit(xv_train, y_train)

    ############### Fetch Assessment Data & Vectorize ######################
    X_test= pd.Series(title)
    xv_test= vectorization.transform(X_test)

    ############## Assessment #####################
    def prediction(X_test, model_object):
        y_pred= model_object.predict(xv_test)
        # print("Predicted values: ")
        return y_pred
    ##############################################
    y_pred_gini=prediction(xv_test, model_gini)
    severity_label=y_pred_gini
    return severity_label
############################ *************SEVERITY ENDS************* #######################################

##############################*********************CRON JOB SCRIPT*********************#######################################################

today= date.today()
cron_job_date_=f'{today.strftime("%b-%d-%Y")}'
def fetch_info_gnews(keywords):          
    len_=len(keywords)
    connect_=sqlite3.connect('timeline-data.db')
    cursor_=connect_.cursor()

    for i in range(0, len_):
        # def find_event_gnews(keyword):
        res = requests.get('https://news.google.com/rss/search?q='f'{keywords[i]}''&hl=en-IN&gl=IN&ceid=IN:en')
        data = res.content
        bs = BeautifulSoup(data, 'lxml')
        items = bs.find_all('item')
        

        for index, item in enumerate(items):
            title = item.title.string
            date_time=item.pubdate.string.split(' ')
            date_=date_time[1]+" "+date_time[2]+" "+date_time[3]
            type_= keywords[i]
            location="none"
            casualty_injured="none"
            tokenized_text = word_tokenize(title)   
            classified_text = st.tag(tokenized_text)
            for word, tag in classified_text:
                if tag=="LOCATION":
                    location=word
            ############################### CASUALTY COUNT - REGEX ##########################################
            ps= PorterStemmer()
            stemmed_output= ' '.join([ps.stem(t) for t in tokenized_text])
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
                    casualty_injured= "Casualty Found - Couldn't detect count of casualities."

                else:
                    casualty_injured= f"Casualties: {temp_1.group()}"

            ####################################################################################################
            
            severity_label=severity_model(title=title)
            set_=(title.lower(), date_, type_.lower(), location.lower(), casualty_injured, severity_label[0].lower(), cron_job_date_)
            cursor_.execute("INSERT INTO Disaster values(?, ?, ?, ?, ?, ?, ?)", set_)
    
            print(f'''
                {index+1}.  Title: {title.lower()}
                    Event Date-time: {date_}
                    Event Type: {type_.lower()}
                    Location: {location.lower()}
                    Casualty/Injured: {casualty_injured}
                    Severity: {severity_label[0].lower()}
                            \n
                ''')


        
        print("\n\n\n")

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
    fetch_info_gnews(keywords_disaster)
    ######################################## ---X-------X------  ################################


#########################################********CRON JOB ENDS*************##############################