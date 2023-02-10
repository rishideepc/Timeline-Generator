import re
import pandas as pd

data= pd.read_excel("Labelled.xlsx")

replacement=(r"/d. ", "")

for i in range(0, 496):
    data["News-Item"][i]=re.sub(r"\d\d. ", "", data["News-Item"][i])
    data["News-Item"][i]=re.sub(r"\d. ", "", data["News-Item"][i])
    print(data["News-Item"][i])

import nltk

nltk.download()





