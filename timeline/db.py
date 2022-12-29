import pyrebase
import genres.generic.gnews
from genres.generic.ndtv import fetch_info_ndtv

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