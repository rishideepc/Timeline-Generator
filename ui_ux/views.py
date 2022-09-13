from pydoc import describe
from flask import Blueprint, render_template
from flask import Flask, request, render_template, redirect
from websites.generic.gnews import *
from websites.generic.ndtv import *
from websites.sports.cricketaddic import fetch_info_cricaddic
import pyrebase
import urllib, json
url ="https://console.firebase.google.com/project/flaskdb-576e5/database/flaskdb-576e5-default-rtdb/data/~2F"


import webbrowser

views= Blueprint('views', __name__)

# @app.route('/')
# @app.route('/', methods=['POST'])

@views.route('/')
def my_form():
    return render_template('base.html')

@views.route('/', methods=['POST'])
def my_form_post():
    text = request.form['keyword']
    text_= request.form['timeframe']
    date_time_=[]
    title=[]
    desc=[]

    # response_=  urllib.urlopen(url)
    # data=json.loads(response_.read())
    # with open('data_landslide.json', 'r') as f:
    #     dicts_=json.load(f)
    # for dict_ in dicts_:
    #     print(dict_['News Feature-landslide'])

    for i in range(0, 100):
        news_features=db.child(f'{today.strftime("%b-%d-%Y")}').child('Disaster-Data').child(f'News Feature-{text}').child(f'News Item-{i+1}').get()
        date_time_.append(news_features[0].val())
        title.append(news_features[2].val())
        desc.append(news_features[1].val())
        

        # news_features=db.child('Disaster-Data').child(f'News Feature-{text}').child(f'News Item-2').get()
        # date_time_2=news_features[0].val()
        # title_2=news_features[2].val()
        # desc_2=news_features[1].val()

        # news_features=db.child('Disaster-Data').child(f'News Feature-{text}').child(f'News Item-3').get()
        # date_time_3=news_features[0].val()
        # title_3=news_features[2].val()
        # desc_3=news_features[1].val()

        # news_features=db.child('Disaster-Data').child(f'News Feature-{text}').child(f'News Item-4').get()
        # date_time_4=news_features[0].val()
        # title_4=news_features[2].val()
        # desc_4=news_features[1].val()


    # date_time_=sorted(date_time_)
            


    
    # return text.upper()
    # with open(f'info.txt', 'w') as f:
    #     f.write(f'Word: {text}')

    #     f.write(f'File Saved: info')

    # print(open("info.txt", 'r').read())

    ############################################################################################
    # if text_!='cricket':
    #     fetch_info_gnews()
    # else:
    #     fetch_info_cricaddic()
    ############################################################################################

    return render_template('timeline.html', title_=title, date_=date_time_, desc_=desc)
    
    # title_1=title_1, date_1=date_time_1, desc_1=desc_1, title_2=title_2, date_2=date_time_2, desc_2=desc_2, title_3=title_3, date_3=date_time_3, desc_3=desc_3, title_4=title_4, date_4=date_time_4, desc_4=desc_4

        

    # processed_text = text.upper()
    # return processed_text
#####################################################


# @views.route('/timeline')
# def call():
#     return render_template('timeline.html')

# def home():
#     return render_template("base.html")



