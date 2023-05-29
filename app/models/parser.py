import sys
sys.path.append('C:\\Users\\HP\\Desktop\\Python_AI\\Timeline_Generator')
import sys
from app.views.endpoints import *


class DataParser:
    def __init__(self):
        pass

    def parse_request(self, request):
        text_keyword = request.form['keyword']
        text_date_time = request.form['timeframe']
        text_location = request.form['location']
        text_features = request.form['features']
        return text_keyword, text_date_time, text_location, text_features

    def parse_db_data(self, items, bounds):
        date = []
        title = []
        desc = []
        casualty_injured = []
        severity = []
        summary = []
        location = []
        _latitude= []
        _longitude= []
        temperature= []
        wind= []
        rain= []

        no_items = 0
        visited = {}
        for item in items:
            latitude, longitude = float(item[9]), float(item[10])
            if bounds[1] <= latitude <= bounds[3] and bounds[0] <= longitude <= bounds[2]:
                group = (item[1][:16], item[3])
                if group in visited:
                    if item[0] not in desc[visited[group]]:
                        desc[visited[group]] += "; " + item[0]
                    continue
                visited[group] = no_items
                title.append(item[2])
                desc.append(item[0])
                casualty_injured.append(item[4])
                severity.append(item[5])
                summary.append(item[6])
                location.append(item[3])
                _latitude.append(item[9])
                _longitude.append(item[10])
                temperature.append(item[11])
                wind.append(item[12])
                rain.append(item[13])
                date.append(item[8])
                no_items += 1
        return title, desc, casualty_injured, severity, summary, no_items, location, _latitude, _longitude, temperature, wind, rain, date
