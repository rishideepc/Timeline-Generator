from pydoc import describe
from flask import Blueprint, render_template
from flask import Flask, request, render_template, redirect
# from genres.generic.gnews import *
# from genres.generic.ndtv import *
# from genres.sports.cricketaddic import fetch_info_cricaddic
import urllib, json
import sqlite3
import webbrowser

views = Blueprint('views', __name__)


@views.route('/')
def my_form():
    return render_template('base.html')

@views.route('/about')
def my_form_about():
    return render_template('about.html')


@views.route('/', methods=['POST'])
def my_form_post():
    connect_ = sqlite3.connect('timeline-data.db')
    cursor_ = connect_.cursor()
    text_keyword = request.form['keyword']
    text_date_time = request.form['timeframe']
    text_location = request.form['location']
    text_features = request.form['features']

    # date_time_ = []
    title = []
    desc = []
    casualty_injured= []
    severity= []
    summary= []

    features_timeline = []
    features_timeline = text_features.split(" ")

    cursor_.execute(f'''

        SELECT * FROM Landslide WHERE (Type LIKE '{text_keyword}' AND Location LIKE '{text_location}') OR (Type LIKE '{text_keyword}')

    ''')

        # SELECT * FROM Disaster WHERE Type LIKE '{text_keyword}' AND Location LIKE '{text_location}'


    items = cursor_.fetchall()

    no_items = 0
    visited = {}
    for item in items:
        group = (item[1][:16], item[3])
        if group in visited:
            if item[0] not in desc[visited[group]]:
                desc[visited[group]] += "; " + item[0]
            continue
        visited[group] = no_items
        title.append(item[2])
        # date_time_.append(item[1])
        desc.append(item[0])
        casualty_injured.append(item[4])
        severity.append(item[5])
        summary.append(item[6])
        no_items += 1

    connect_.commit()
    connect_.close()

    return render_template('timeline.html', title_=title, desc_=desc, num=no_items, casualty_injured_=casualty_injured, severity_=severity, summary_=summary, features_=features_timeline)
