from flask import request, render_template
from app import app
from app.models.dao import DAOOperations
from app.models.parser import DataParser


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
        text_keyword, text_date_time, text_location, text_features = parser.parse_request(request)
        items = dao.query_all(text_keyword, text_location)
        title, desc, casualty_injured, severity, summary, no_items = parser.parse_db_data(items)
        features_timeline = text_features.split(" ")
        return render_template('timeline.html', title_=title, desc_=desc, num=no_items,
                               casualty_injured_=casualty_injured, severity_=severity, summary_=summary,
                               features_=features_timeline)
