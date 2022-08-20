from ast import keyword
from flask import Blueprint, render_template
from flask import Flask, request, render_template, redirect
from websites.generic.ndtv import *
from websites.sports.cricketaddic import find_event_cric

def addition():
    return 1+1

views= Blueprint('views', __name__)

@views.route('/')


# @app.route('/')

####################################################
def my_form():
    return render_template('base.html')

# @app.route('/', methods=['POST'])


@views.route('/', methods=['POST'])
def my_form_post():
    text = request.form['keyword']

    
    # return text.upper()
    # with open(f'info.txt', 'w') as f:
    #     f.write(f'Word: {text}')

    #     f.write(f'File Saved: info')

    # print(open("info.txt", 'r').read())
    if text!='cricket':
        find_event(keyword=text)
    else:
        find_event_cric()

    return redirect('/')

    # processed_text = text.upper()
    # return processed_text
#####################################################




# def home():
#     return render_template("base.html")



