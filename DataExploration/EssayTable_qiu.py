import pandas as pd
import re
import nltk, string
from nltk.corpus import brown
from nltk.corpus import stopwords
from nltk import FreqDist
from operator import itemgetter
import numpy as np
from __future__ import division

data = pd.read_csv("opendata_essays.csv")
data.head()
data[:3] #subset the first 4 rows of the data set'''
data.lookup([1,2], ["title","essay"]) #exact element: row 1, title; row 2, essay

'''
#fastest project: completed in a day
e565fb42185c6e9f22806ad9d5ac8a77

data[data["_projectid"] == '"e565fb42185c6e9f22806ad9d5ac8a77"']
#row number of the this data. 

'''
x = data["_projectid"]
y = '"e565fb42185c6e9f22806ad9d5ac8a77"'
matchIndex = [ i for i, x in enumerate(x) if x ==  y] 

essay = data.lookup(matchIndex, ["essay"])

## Data Cleaning
essayString = "".join([i if i !="\n" else "\r" for i in essay])
essayClean = re.sub("\\r|\\\\n", "", essayString)


##nltk package
## Tokenize words, Remove stop words, punctuations

words = nltk.word_tokenize(essayClean)
essayNltk = nltk.Text(words)
stopwords = nltk.corpus.stopwords.words('english')
words = [word for word in words if word not in stopwords]

def allPunct(x):
    return(all([char in string.punctuation for char in x]))

def removePunct(text):
    return([w for w in text if not allPunct(w)]) 

words = removePunct(words)
## Identifying Unique Words
uniqueWords = sorted(set(words))

## Distribution of Words
fdistWords = FreqDist(words)
print fdistWords

wordsFreq = [(x, fdistWords[x]) for x in uniqueWords]
wordsFreq.sort(key=operator.itemgetter(1),reverse=True)


## Common words pairing
words.collocation()

