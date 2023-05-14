import sys
sys.path.append('C:\\Users\\HP\\Desktop\\Python_AI\\Timeline_Generator')
import googlemaps
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
        # date_time_ = []
        title = []
        desc = []
        casualty_injured = []
        severity = []
        summary = []
        location = []

        no_items = 0
        visited = {}
        for item in items:
            # geocode_lower_location= gmaps.geocode(item[3])
            # latitude = geocode_result_2[0]['geometry']['location']['lat']
            # longitude = geocode_result_2[0]['geometry']['location']['lng']
            params_2= {
                'access_key': access_key,
                'query': item[3],
                'limit': 1            
            }
            response= requests.get(endpoint, params=params_2).json()
            latitude, longitude= response['data'][0]['latitude'], response['data'][0]['longitude']
            if bounds[1] <= latitude <= bounds[3] and bounds[0] <= longitude <= bounds[2]:
                #
                group = (item[1][:16], item[3])
                if group in visited:
                    if item[0] not in desc[visited[group]]:
                        desc[visited[group]] += "; " + item[0]
                    continue
                visited[group] = no_items
                #
                title.append(item[2])
                # date_time_.append(item[1])
                desc.append(item[0])
                casualty_injured.append(item[4])
                severity.append(item[5])
                summary.append(item[6])
                location.append(item[3])
                no_items += 1
        return title, desc, casualty_injured, severity, summary, no_items, location