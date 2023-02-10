# import openpyxl
# import nltk
# from nltk.corpus import stopwords, wordnet
# nltk.download("stopwords")
# nltk.download('averaged_perceptron_tagger')
# stop_words = stopwords.words("english")
# from nltk.stem import WordNetLemmatizer
# lemmatizer = WordNetLemmatizer()
# filename = "C:\\Users\\HP\\Desktop\\Python_AI\\Timeline_Generator\\Labelled.xlsx"

# workbook = openpyxl.load_workbook(filename)

# worksheet = workbook.active

# data = {}
# labelled = {}

# def get_wordnet_pos(word):
#     """Map POS tag to first character lemmatize() accepts"""
#     tag = nltk.pos_tag([word])[0][1][0].upper()
#     tag_dict = {"J": wordnet.ADJ,
#                 "N": wordnet.NOUN,
#                 "V": wordnet.VERB,
#                 "R": wordnet.ADV}
#     return tag_dict.get(tag, wordnet.NOUN)

# for row in worksheet.iter_rows(1, worksheet.max_row, values_only=True):
#     sentence = row[0]
#     label = row[1]
#     if sentence and label:
#         sentence = ".".join(sentence.split(".")[1:])
#         sentence = nltk.word_tokenize(sentence)
#         cleaned = [x.lower() for x in sentence if x not in stop_words]
#         cleaned = [lemmatizer.lemmatize(x, get_wordnet_pos(x)) for x in cleaned]
#         cleaned = [x for x in cleaned if x.isalpha()]
#         cleaned = " ".join(list(set(cleaned)))
#         if cleaned not in data:
#             data[cleaned] = set()
#         data[cleaned].add(label)
#         if label not in labelled:
#             labelled[label] = set()
#         labelled[label].add(cleaned)

# print("Unique News Heading Count by Label")
# for label in labelled:
#     print(label, len(labelled[label]))

# print("Total Unique News Headings", len(data))

# print("Incorrectly labelled data")
# c = 0
# for sentence in data:
#     x = len(data[sentence])
#     if x > 1:
#         print(sentence, x, data[sentence])
#         c += 1

# print("Total incorrectly labelled data", c)

from word2number import w2n

print(w2n.word_to_num('hello i am two, three'))
