from ast import keyword
from xmlrpc.client import DateTime
import requests
from bs4 import BeautifulSoup
import urllib, json
import time
from datetime import *
import re
######################### *******NER Import********** #################################
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
#######################################################################################
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, precision_recall_curve
from sklearn.naive_bayes import GaussianNB
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
########################################## *****IMPORT ENDS***** ############################################################################

############## ******************TRAINING THE SEVERITY MODEL*********************** #########################
def severity_model():
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
    ###################### Training #################################################
    X_train= data['News-Item']  # Feature Column
    y_train= data['Label']  # Target Colum
    X_train, X_test, y_train, y_test= train_test_split(data['News-Item'], data['Label'], test_size=0.15, random_state=35)
    ###################### Vectorization && Transformation ####################################
    vectorization= TfidfVectorizer()
    xv_train= vectorization.fit_transform(X_train)
    xv_test= vectorization.transform(X_test)

    # model_gini= DecisionTreeClassifier(criterion="gini", random_state=123, max_depth=10, min_samples_leaf=6)
    # model_gini= RandomForestClassifier(criterion="gini", n_estimators=50, max_depth=10, min_samples_leaf=6)
    model_gini=svm.SVC(kernel='linear')

    model_gini.fit(xv_train, y_train)
    y_pred= model_gini.predict(xv_test)
    # print("\nPredicted: ", y_pred)
    # print("\nTest: ", y_test)
    print("\nConfusion Matrix: ", confusion_matrix(y_test, y_pred))
    print("\nAccuracy Score: ", accuracy_score(y_test, y_pred)*100, "%")
    print("\nPrecision: ", precision_score(y_test, y_pred, average="weighted")*100, "%")
    print("\nRecall: ", recall_score(y_test, y_pred, average="weighted")*100, "%")
    print("\nF1 Score: ", f1_score(y_test, y_pred, average="weighted")*100, "%")
    
    # pickle.dump(model_gini, open('severity_model.pkl', 'wb'))
    # return vectorization
    ############################ Training ends ###################################

    
    # ############### Fetch Assessment Data & Vectorize ######################
    # X_test= pd.Series(title)
    # xv_test= vectorization.transform(X_test)

    # ############## Assessment #####################
    # def prediction(X_test, model_object):
    #     y_pred= model_object.predict(xv_test)
    #     # print("Predicted values: ")
    #     return y_pred
    # ##############################################
    # y_pred_gini=prediction(xv_test, model_gini)
    # severity_label=y_pred_gini
    # return severity_label
    ##########################################################################


############################ *************SEVERITY ENDS************* #######################################


# vectorized = severity_model()
severity_model()