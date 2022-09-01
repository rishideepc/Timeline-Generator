from ast import keyword
import requests
import json
from bs4 import BeautifulSoup
import pyrebase
import urllib, json
import time
config= {
                "apiKey": "AIzaSyAMl-ofcpcF0zO3KmwAMuVYYFs-UqjWBCY",
                "authDomain": "flaskdb-576e5.firebaseapp.com",
                "databaseURL": "https://flaskdb-576e5-default-rtdb.asia-southeast1.firebasedatabase.app",
                "projectId": "flaskdb-576e5",
                "storageBucket": "flaskdb-576e5.appspot.com",
                "messagingSenderId": "1096383217352",
                "appId": "1:1096383217352:web:243a244f597003ad566ffd"
}
firebase=pyrebase.initialize_app(config)

db=firebase.database()

# keywords for disaster class
# keywords_disaster=['landslide', 'flood', 'earthquake', 'tsunami', 'flash flood']
keywords_disaster=['landslide']

#####################################################
# cronjob script

def fetch_info_gnews(keywords):          
    len_=len(keywords)
    for i in range(0, len_):
        # def find_event_gnews(keyword):
        res = requests.get('https://news.google.com/rss/search?q='f'{keywords[i]}''&hl=en-IN&gl=IN&ceid=IN:en')
        data = res.content
        bs = BeautifulSoup(data, 'lxml')
        items = bs.find_all('item')
        for index, item in enumerate(items):
            title = item.title.string
            datetime = item.pubdate.string
            type_= keywords[i]

            db.child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(f'News Item-{index+1}').update({"Title":title})
            db.child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(f'News Item-{index+1}').update({"Date-Time":datetime})
            db.child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(f'News Item-{index+1}').update({"Type":type_})

            # x=db.child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(f'News Item-{index+1}').get()
            # x_=x.val()
            print(f'''
                {index+1}.  Title: {title}
                    Event Date-time: {datetime}
                    Event Type: {type_}
                            \n
                ''')

        print("\n\n\n")


######################################################


if __name__=="__main__":
    
    fetch_info_gnews(keywords_disaster)
    # time.sleep(10)
    # url="https://console.firebase.google.com/project/flaskdb-576e5/database/flaskdb-576e5-default-rtdb/data/~2F"
    # response_=  urllib.urlopen(url)
    # data=json.loads(response_.read())
    # print(data)
    # r=requests.get()
    # print(r.json())