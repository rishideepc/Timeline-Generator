from ast import keyword
from xmlrpc.client import DateTime
import requests
from bs4 import BeautifulSoup
import urllib, json
import datetime
from datetime import *
import re
import psutil
from memory_profiler import profile
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
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
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
@profile
def severity_model():
    start= datetime.now()
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

    # model_gini= DecisionTreeClassifier(criterion="gini")
    # model_gini= RandomForestClassifier(criterion="gini")
    # model_gini=svm.SVC(kernel='linear')

    # model_gini= OneVsRestClassifier(DecisionTreeClassifier())
    # model_gini= OneVsRestClassifier(RandomForestClassifier())
    # model_gini = OneVsRestClassifier(svm.SVC())
    # model_gini = OneVsRestClassifier(KNeighborsClassifier(n_neighbors=3))
    # model_gini = OneVsRestClassifier(SGDClassifier())
    model_gini = OneVsRestClassifier(MLPClassifier())

    model_gini.fit(xv_train, y_train)
    y_pred= model_gini.predict(xv_test)
    # print("\nPredicted: ", y_pred)
    # print("\nTest: ", y_test)
    end= datetime.now()
    memory_used=psutil.virtual_memory()[3]/1000000000

    print("\nConfusion Matrix: ", confusion_matrix(y_test, y_pred))
    print("\nAccuracy Score: ", accuracy_score(y_test, y_pred)*100, "%")
    print("\nPrecision: ", precision_score(y_test, y_pred, average="weighted")*100, "%")
    print("\nRecall: ", recall_score(y_test, y_pred, average="weighted")*100, "%")
    print("\nF1 Score: ", f1_score(y_test, y_pred, average="weighted")*100, "%")
    td=(end - start).total_seconds() *10**3
    print(f"\nExecution Time: {td:.03f}ms") 
    print("\nMemory Used (GB): ", memory_used)

    
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
if __name__=="__main__":
    severity_model()
    process= psutil.Process()
    memory_usage= process.memory_info().rss / 1024 / 1024
    print(f"Total memory usage: {memory_usage:.2f} MB")