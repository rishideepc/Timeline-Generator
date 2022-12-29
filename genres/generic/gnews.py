from ast import keyword
from xmlrpc.client import DateTime
import requests
from bs4 import BeautifulSoup
# import pyrebase
import urllib, json
import time
from datetime import *

# ########################################
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
# ########################################

import sqlite3

st = StanfordNERTagger('C:\\Users\\HP\\Desktop\\Python_AI\\Timeline_Generator\\timeline\\templates\\stanford-ner-2020-11-17\\classifiers\\english.all.3class.distsim.crf.ser.gz',
					   'C:\\Users\\HP\\Desktop\\Python_AI\\Timeline_Generator\\timeline\\templates\\stanford-ner-2020-11-17\\stanford-ner.jar',
					   encoding='utf-8')

# keywords for disaster class
keywords_disaster=['landslide', 'earthquake', 'tsunami', 'flood']

#####################################################
# cronjob script
today= date.today()
cron_job_date_=f'{today.strftime("%b-%d-%Y")}'
def fetch_info_gnews(keywords):          
    len_=len(keywords)
    connect_=sqlite3.connect('timeline-data.db')
    cursor_=connect_.cursor()

    for i in range(0, len_):
        # def find_event_gnews(keyword):
        res = requests.get('https://news.google.com/rss/search?q='f'{keywords[i]}''&hl=en-IN&gl=IN&ceid=IN:en')
        data = res.content
        bs = BeautifulSoup(data, 'lxml')
        items = bs.find_all('item')
            ###################################################################################
            ## convert str to datetime.datetime object and sort in firebase
            ###################################################################
            # date_time = datetime.strptime(date_time_str, '%a, %d %b %Y %H:%M:%S %Z')
            # date_time.sort()
            # print(type(date_time))
            # date_time = json.dumps(date_time, default=str)
            # print(type(date_time))
            # date_time.sort()
            #################################################################
            # class DTEncoder(json.JSONEncoder):
            #         def default(self, obj):
            #             #  if passed in object is datetime object
            #             # convert it to a string
            #             if isinstance(obj, datetime):
            #                 return str(obj)
            #             #  otherwise use the default behavior
            #             return json.JSONEncoder.default(self, obj)

            # date_time = json.dumps(date_time, cls=DTEncoder)
            # print(type(date_time))
            ###################################################################################

################################################################################################
        

        for index, item in enumerate(items):
            title = item.title.string
            date_time=item.pubdate.string.split(' ')
            date_=date_time[1]+" "+date_time[2]+" "+date_time[3]
            type_= keywords[i]
            location="None"
            severity="None"
            tokenized_text = word_tokenize(title)   
            classified_text = st.tag(tokenized_text)
            for word, tag in classified_text:
                if tag=="LOCATION":
                    # db.child(f'{today.strftime("%b-%d-%Y")}').child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(f'News Item-{index+1}').update({"Location":word})
                    location=word

            #defining severity
            # x=0
            # adjective="None"
            # if f"past {x} years" in title:
            #     if x>15:
            #         severity="Very High"
            #     elif x>10:
            #         severity="High"
            # elif f"{adjective} in {x} years" in title:
            #     if adjective=="greatest" or adjective=="highest" or adjective=="largest" or adjective=="worst":
            #         if x>15:
            #             severity="Very High"
            #         elif x>10:
            #             severity="High"
            #     else:
            #         severity="Can't determine severity with accuracy"
            
            # elif f"{x} people" or f"{x} people affected" or f"{x} people dead" in title:
            #     if x>15:
            #         severity="Very High"
            #     elif x>10:
            #         severity="High"
            #     else:
            #         severity="Moderate"            

            # elif "collapse" in title:
            #     severity="Moderate"

            # else:
            #     severity="Low"

            #ending severity definition

            set_=(title, date_, type_, location, severity, cron_job_date_)
            cursor_.execute("INSERT INTO Disaster values(?, ?, ?, ?, ?, ?)", set_)
    
            # db.child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(location).child(f'News-Item-{index+1}').update({"Title":title})
            # db.child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(location).child(f'News-Item-{index+1}').update({"Date-Time":date_time})
            # db.child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(location).child(f'News-Item-{index+1}').update({"Type":type_})
            # db.child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(location).child(f'News-Item-{index+1}').update({"CronJob-Date":cron_job_date_})




            # db.child(f'{today.strftime("%b-%d-%Y")}').child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(f'News Item-{index+1}').update({"Title":title})
            # db.child(f'{today.strftime("%b-%d-%Y")}').child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(f'News Item-{index+1}').update({"Date-Time":date_time})
            # db.child(f'{today.strftime("%b-%d-%Y")}').child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(f'News Item-{index+1}').update({"Type":type_})
            # db.child(f'{today.strftime("%b-%d-%Y")}').child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(f'News Item-{index+1}').update({"Location":""})
            
            
            
            # x=db.child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(f'News Item-{index+1}').get()
            # x_=x.val()
            print(f'''
                {index+1}.  Title: {title}
                    Event Date-time: {date_}
                    Event Type: {type_}
                    Location: {location}
                            \n
                ''')


        
        print("\n\n\n")

###############################################################################################

        # for i in range(1, 101):
        #     if i!=100:
        #         for j in range(i+1, 101):
        #             x=db.child(f'{today.strftime("%b-%d-%Y")}').child('Disaster-Data').child(f'News Feature-{keywords[i]}').child(f'News Item-{j}').child('Location').get().val()
        #             db.child(f'{today.strftime("%b-%d-%Y")}').child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(f'News Item-{i}').order_by_key().order_by_child('Location').equal_to(x).remove()
        #             break

        # for i in range(1, 100):
        #     if i!=99:
        #         for j in range(i+1, 101):
        #             db.child(f'{today.strftime("%b-%d-%Y")}').child("Disaster-Data").child(f'News Feature-{keywords[i]}').child(f'News Item-{i}').order_by_key().order_by_child('Location').equal_to(arr_[j]).remove()
                    
        #             break


            
        # def Remove(duplicate):
        #     final_list = []
        #     for num in duplicate:
        #         if num not in final_list:
        #             final_list.append(num)
        #         return final_list

#########################################################################
#     cursor_.execute('''

# SELECT * FROM Disaster

# ''')
#     items=cursor_.fetchall()
#     len_=len(items)
#     for i in range(0, len_):
#         if i!=len_-1:
#             for j in range(i+1, len_):
#                 if(items[j][1]==items[i][1]):
#                     items[i][1]="null"

#         else:
#             break


    connect_.commit()
    connect_.close()

if __name__=="__main__":

    ########################################  **FUNCTION CALL**   ################################
    fetch_info_gnews(keywords_disaster)
    ######################################## ---X-------X------  ################################