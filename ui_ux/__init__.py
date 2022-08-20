from cgitb import text
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from os import *
from flask import Flask, request, render_template
from ui_ux.views import my_form_post
from flask import request





def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']= "Python Web-Scrapper"
    
    
    # word=my_form_post.processed_text
    # print(word)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    
    return app

