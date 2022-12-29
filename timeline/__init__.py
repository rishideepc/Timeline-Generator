from cgitb import text
from flask import Flask
from os import *
from flask import Flask, request, render_template
from timeline.views import my_form_post
from flask import request





def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']= "Python Web-Scrapper"

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    
    return app

