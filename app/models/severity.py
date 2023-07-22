from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve, ConfusionMatrixDisplay, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, precision_recall_curve

import matplotlib.pyplot as plt
import re


def plot_roc_curve(true_y, y_prob):
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(3):
        fpr[i], tpr[i], _ = roc_curve(true_y[:, i], y_prob[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    plt.figure()
    classes = ["high", "low", "uncertain"]
    for i in range(3):
        plt.plot(fpr[i], tpr[i], label=f'Class {classes[i]}(area = {roc_auc[i]:.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc="lower right")
    plt.show()


def severity_model():
    data = pd.read_excel('..\\resources\\Labelled.xlsx')

    for j in range(0, 818):
        data['Label'][j] = data['Label'][j].lower()
        data['Label'][j] = re.sub(" ", "", data['Label'][j])
        data['News-Item'][j] = re.sub('https?://\S+|www\.\S+', '', data['News-Item'][j])
        data['News-Item'][j] = re.sub('\[.*?\]', '', data['News-Item'][j])
        data['News-Item'][j] = re.sub('<.*?>+', '', data['News-Item'][j])
        data['News-Item'][j] = re.sub('\w*\d\w*', '', data['News-Item'][j])

    y = label_binarize(data['Label'], classes=["high", "low", "uncertain"])

    X_train, X_test, y_train, y_test = train_test_split(data['News-Item'], y, test_size=0.15,
                                                        random_state=35)
    vectorization = TfidfVectorizer()
    xv_train = vectorization.fit_transform(X_train)
    xv_test = vectorization.transform(X_test)

    # model_gini= OneVsRestClassifier(DecisionTreeClassifier())
    # model_gini= OneVsRestClassifier(RandomForestClassifier())
    # model_gini = OneVsRestClassifier(svm.SVC())
    # model_gini = OneVsRestClassifier(KNeighborsClassifier(n_neighbors=3))
    # model_gini = OneVsRestClassifier(SGDClassifier())
    model_gini = OneVsRestClassifier(MLPClassifier())

    model_gini.fit(xv_train, y_train)
    y_pred = model_gini.predict(xv_test)
    cm = confusion_matrix(y_test.argmax(axis=1), y_pred.argmax(axis=1))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model_gini.classes_)
    disp.plot()
    plt.show()
    # print("\nConfusion Matrix: ", )
    print("\nAccuracy Score: ", accuracy_score(y_test, y_pred) * 100, "%")
    print("\nPrecision: ", precision_score(y_test, y_pred, average="weighted") * 100, "%")
    print("\nRecall: ", recall_score(y_test, y_pred, average="weighted") * 100, "%")
    print("\nF1 Score: ", f1_score(y_test, y_pred, average="weighted") * 100, "%")

    # pickle.dump(model_gini, open('severity_model.pkl', 'wb'))
    # return vectorization
    plot_roc_curve(y_test, y_pred)
    print(f'model 1 AUC score: {roc_auc_score(y_test, y_pred)}')


# vectorized = severity_model()
severity_model()
