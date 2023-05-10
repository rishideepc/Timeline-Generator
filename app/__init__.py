import sys
sys.path.append('/home/rishideepch/Documents/Work_Internship/Timeline-Generator/')

from flask import Flask
import os

template_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(template_dir, 'templates')
app = Flask(__name__, template_folder=template_dir)

from app.views.endpoints import *

if __name__ == '__main__':
    app.run()


