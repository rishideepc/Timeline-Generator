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
##################################################
# import requests
# import json
# from bs4 import BeautifulSoup

# res = requests.get('https://news.google.com/rss/search?q=green+technology&hl=en-IN&gl=IN&ceid=IN:en')
# data = res.content
# bs = BeautifulSoup(data)
# items = bs.find_all('item')
# for item in items:
#     title = (item.description.string)
#     print(title)
#     print("\n")
###################################################
# import json
# with open('data_landslide.json', 'r') as f:
#         dicts_=json.loads(f)
# for dict_ in dicts_:
#     print(dict_['News Feature-landslide'])


# import spacy
# from spacy import displacy
# nlp = spacy.load('en_core_web_sm')

# doc = nlp("Thodupuzha: All five members of a family, who were trapped under debris following a landslide in Kudayathoor near Thodupuzha, were found dead after a five-hour-long search."
#           "The deceased are Maliyekal Soman, his mother Thankamma, wife Shiji, daughter Shima and her son Devanand (4).  Their house was washed away after the landslide hit the area in the early hours of Monday."
#           "As per reports, the road and crops in the area have been washed away in the landslide.")

# for entity in doc.ents:
#     if entity.label_ == "GPE":
#         print(entity.text)


# arr=[1, 1, 3]
# print(enumerate(arr))

# """
# Thankamma



arr=[1, 12, 4, 1, 5, 6, 4]

for i in range(0, 6):
    for j in range(i+1, 6):
        if (arr[i]==arr[j]):
            arr[i]=="*"

        


