import requests
import json
from bs4 import BeautifulSoup

keywords=['landslide', 'flood', 'earthquake']
# def find_event_gnews(keyword):
res = requests.get('https://news.google.com/rss/search?q='f'{keywords[0]}''&hl=en-IN&gl=IN&ceid=IN:en')
data = res.content
bs = BeautifulSoup(data, 'lxml')
items = bs.find_all('item')
for index, item in enumerate(items):
    title = item.title.string
    datetime = item.find('pubDate')
    type_= keywords[0]
    print(f'''
        {index+1}.  Title: {title}
             Event Date-time: {datetime}
             Event Type: {type_}
                    \n
        ''')