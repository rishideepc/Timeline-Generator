import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.metrics import accuracy_score
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import seaborn as sns
import re
import sqlite3


data= pd.read_excel('C:/Users/HP/Desktop/Python_AI/Timeline_Generator/genres/generic/severity_label/Labelled.xlsx')

################################ Data cleansing ##################################
for i in range(0, 596):
    data['Label'][i]=data['Label'][i].lower()
    data['Label'][i]=re.sub(" ", "", data['Label'][i])
    data['News-Item'][i]=re.sub('https?://\S+|www\.\S+', '', data['News-Item'][i])
    data['News-Item'][i]=re.sub('\[.*?\]', '', data['News-Item'][i])
    data['News-Item'][i]=re.sub('<.*?>+', '', data['News-Item'][i])
    data['News-Item'][i]=re.sub('\w*\d\w*', '', data['News-Item'][i])  
############################### XXXXXXXXXXXXXXXX #################################

X= data['News-Item']  # Feature Column
y= data['Label']  # Target Column


X_train, X_test, y_train, y_test= train_test_split(X, y, test_size=0.2)
print(type(X_test))


vectorization= TfidfVectorizer()
xv_train= vectorization.fit_transform(X_train)
# print(xv_train)
xv_test= vectorization.transform(X_test)


###########################################################################
def prediction(X_test, model_object):
    y_pred= model_object.predict(xv_test)
    print("Predicted values: ")
    print(y_pred)
    return y_pred

def cal_accuracy(y_test, y_pred):
    # print("Confusion Matrix: ", confusion_matrix(y_test, y_pred))
    print("Accuracy: ", accuracy_score(y_test, y_pred)*100) 
############################################################################

### using criterion GINI/ENTROPY with Decision Tree/ Random Forest/ SVM ########################################
# model_gini= DecisionTreeClassifier(criterion="gini", random_state=123, max_depth=10, min_samples_leaf=6)
# model_gini=RandomForestClassifier(n_estimators=25, criterion='entropy', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None,bootstrap=True, oob_score=False, n_jobs=1, random_state=None, verbose=0, warm_start=False,class_weight=None)
model_gini=svm.SVC(kernel='linear')
model_gini.fit(xv_train, y_train)
y_pred_gini=prediction(xv_test, model_gini)
cal_accuracy(y_test, y_pred_gini)
##################################################################




# earthquake: 
# <5: Low
# 5.0-6.0: Medium
# 6.1-6.9: High
# >7: Very high
