import sys
sys.path.append('C:\\Users\\HP\\Desktop\\Python_AI\\Timeline_Generator')
from flask import request, render_template
from app import app
from app.models.dao import DAOOperations
from app.models.parser import DataParser
import requests


@app.route('/about')
def my_form_about():
    return render_template('about.html')


@app.route('/', methods=['POST', 'GET'])
def my_form_post():
    if request.method == "GET":
        return render_template('base.html')
    elif request.method == "POST":
        dao = DAOOperations()
        parser = DataParser()
        # text_keyword, text_date_time, text_location = parser.parse_request(request)
        text_keyword= request.form['keyword']
        text_date_time= request.form['timeframe']
        text_location= request.form['location']

        # Bounding box for the parent location
        # geocode_greater_location= gmaps.geocode(text_location)
        # bounds= geocode_greater_location[0]['geometry']['bounds']
        # sw_lat= bounds['southwest']['lat']
        # sw_lng= bounds['southwest']['lng']
        # ne_lat= bounds['northeast']['lat']
        # ne_lng= bounds['northeast']['lng']
        params_1= {
            'access_key': access_key,
            'query': text_location,     
            'limit': 1,
            'bbox_module': '1'
        }
        response = requests.get(endpoint, params=params_1).json()
        bounds = response['data'][0]['bbox_module']

        # text_features= []
        text_features= request.form.getlist('features[]')
        items = dao.query_all(text_keyword, text_location)
        title, desc, casualty_injured, severity, summary, no_items, location = parser.parse_db_data(items, bounds)
        # features_timeline = text_features.split(" ")
        return render_template('timeline.html', title_=title, desc_=desc, num=no_items,
                               casualty_injured_=casualty_injured, severity_=severity, summary_=summary,
                               features_=text_features, location_=location)
