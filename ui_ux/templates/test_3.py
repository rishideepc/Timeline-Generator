# from bs4 import BeautifulSoup
# import requests
# from nltk.tag import StanfordNERTagger
# from nltk.tokenize import word_tokenize

# # res = requests.get('https://news.google.com/rss/search?q=landslide&hl=en-IN&gl=IN&ceid=IN:en')
# # data = res.content
# # bs = BeautifulSoup(data)
# # items = bs.find_all('item')
# # for item in items:
# #     text = str(item.title)
# #     date = str(item.pubdate)
# #     # results = {1: spacy_ner(text), 2: grograpy3_ner(text), 3: stanford_ner(text)}
# #     print(text, date, stanford_ner(text))


from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

st = StanfordNERTagger('C:\\Users\\HP\\Desktop\\Python_AI\\Timeline_Generator\\ui_ux\\templates\\stanford-ner-2020-11-17\\classifiers\\english.all.3class.distsim.crf.ser.gz',
					   'C:\\Users\\HP\\Desktop\\Python_AI\\Timeline_Generator\\ui_ux\\templates\\stanford-ner-2020-11-17\\stanford-ner.jar',
					   encoding='utf-8')

text = 'While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal.'

tokenized_text = word_tokenize(text)
classified_text = st.tag(tokenized_text)

# print(classified_text)

for word, tag in classified_text:
	if tag=="LOCATION":
		print(word)





# print(classified_text)

# from geograpy import extraction

# e = extraction.Extractor(text="Thodupuzha: All five members of a family, who were trapped under debris following a landslide in Kudayathoor near Thodupuzha, were found dead after a five-hour-long search."
#           "The deceased are Maliyekal Soman, his mother Thankamma, wife Shiji, daughter Shima and her son Devanand (4).  Their house was washed away after the landslide hit the area in the early hours of Monday."
#           "As per reports, the road and crops in the area have been washed away in the landslide.")

# e.find_entities()
# print (e.places)

# """
# ['Thodupuzha', 'Kudayathoor', 'Thodupuzha', 'Maliyekal Soman', 'Shiji', 'Shima', 'Devanand']
# """

# from datetime import *

# today= date.today()
# cron_job_date_=f'{today.strftime("%b-%d-%Y")}'
# print(cron_job_date_)