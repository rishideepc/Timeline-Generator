import sys
import pandas as pd
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import pickle


def severity_model():
    data = pd.read_excel('..\\resources\\Labelled.xlsx', engine='openpyxl')

    for j in range(0, 596):
        data['Label'][j] = data['Label'][j].lower()
        data['Label'][j] = re.sub(" ", "", data['Label'][j])
        data['News-Item'][j] = re.sub('https?://\S+|www\.\S+', '', data['News-Item'][j])
        data['News-Item'][j] = re.sub('\[.*?\]', '', data['News-Item'][j])
        data['News-Item'][j] = re.sub('<.*?>+', '', data['News-Item'][j])
        data['News-Item'][j] = re.sub('\w*\d\w*', '', data['News-Item'][j])
    X_train = data['News-Item']  # Feature Column
    y_train = data['Label']  # Target Colum
    vectorization = TfidfVectorizer()
    xv_train = vectorization.fit_transform(X_train)
    model_gini = svm.SVC(kernel='linear')
    model_gini.fit(xv_train, y_train)
    pickle.dump(model_gini,
                open('..\\resources\\severity_model.pkl', 'wb'))
    return vectorization


vectorized = severity_model()
