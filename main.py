import time
from timeline.views import my_form_post
from genres.generic.ndtv import *
from genres.sports.cricketaddic import *
from timeline import create_app
from flask import request

app=create_app()

if __name__=="__main__":

    app.run(debug=True)