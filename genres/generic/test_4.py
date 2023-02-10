import sqlite3
from nltk.stem import WordNetLemmatizer, PorterStemmer
import nltk
# nltk.download('wordnet')
connect_=sqlite3.connect('timeline-data.db')
keyword='India'
cursor_=connect_.cursor()

cursor_.execute(f'''

SELECT * FROM Disaster

''')


# WHERE location LIKE '{keyword}'
# print(cursor_.fetchall())
items = cursor_.fetchall()
titles=[]
# print(items)
for index,item in enumerate(items):
#     print(f'''
#     {index+1}
#     Title: {item[0]}
#     DateTime: {item[1]}
#     Type: {item[2]}
#     Location: {item[3]}
#     Casualty Count: {item[4]}
#     Severity: {item[5]}
#     CronJobDate: {item[6]}
#     ''')
    titles.append(item[0])

################# Lemmatization / Tokenization Test Script ###################
sentence_1="death dead died deadly die dies dying"
sentence_2='fear feared fearing fears'
sentence_3='injured injure injury'
sentence_4='kill kills killed killing'
sentence_5='buries buried bury burying burial'
sentence_6='hit hits'
sentence_7='trap trapped trapping'
sentence_8='threat threaten threatening threatens threatened'
sentence_9='hurt hurting hurts'

word_list= nltk.word_tokenize(sentence_9)
print(word_list)
print('\n')
print('Lemmatized Output:')
lemmatizer=WordNetLemmatizer()
lemmatized_output= ' '.join([lemmatizer.lemmatize(w) for w in word_list])
print(lemmatized_output)
print('\n')
print('Stemmed Output: ')
ps= PorterStemmer()
stemmed_output= ' '.join([ps.stem(w) for w in word_list])
print(stemmed_output)
    

connect_.commit()
connect_.close()