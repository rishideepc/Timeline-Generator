# # import webbrowser

# # keyword='cricket'
# # webbrowser.open('https://www.hindustantimes.com/'f'{keyword}''')

# # from ui_ux import create_app

# # app=create_app()

# # if __name__=="__main__":

# #     app.run(debug=True)

# import cgi
# import cgitb #found this but isn't used?

# form = cgi.FieldStorage()

# first_name = form.getvalue('first_name').capitalize()
# last_name  = form.getvalue('last_name').capitalize()

# print ("Content-type:text/html\r\n\r\n")
# print ("<html>")
# print ("<head>")
# print ("<title>Hello - Second CGI Program</title>")
# print ("</head>")
# print ("<body>")
# print ("<h2>Your name is {}. {} {}</h2>".format(last_name, first_name, last_name))
# print ("</body>")
# print ("</html>")


# from bs4 import BeautifulSoup
# import requests

# url= requests.get('https://www.google.com/search?q=india+football+2022+to+2023&tbm=nws')
# soup=BeautifulSoup(url.content, 'lxml')
# heading=soup.find('div', id="main").text.strip()

# # with open("test.txt", 'w') as f:
# #     f.write(heading)
# print(heading)

import requests
import json
from bs4 import BeautifulSoup

res = requests.get('https://news.google.com/rss/search?q=green+technology&hl=en-IN&gl=IN&ceid=IN:en')
data = res.content
bs = BeautifulSoup(data)
items = bs.find_all('item')
for item in items:
    title = (item.description.string)
    print(title)
    print("\n")