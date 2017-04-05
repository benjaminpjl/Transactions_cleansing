# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import numpy as np
import pandas as pd
import os
import nltk
import re
import string
from string import digits
from stemming.porter2 import stem
from collections import Counter
from nltk.tokenize import word_tokenize
from configuration import CONFIG
import gensim


#Change working directory
os.chdir("/Users/benjaminpujol/Documents/Mobillity/Transactions_cleansing")


#Import data 
df = pd.read_csv("data/RAW_TRANSACTION.csv")
print df["description"]

#Get categories:
print df["category"].unique()


#Tokenize description

def make_list(row):
    row = nltk.word_tokenize(row)
    return(row)

def take_first(row): 
    return row.pop(0)

#Set stopwords
nltk.download('stopwords')
stpwds = set(nltk.corpus.stopwords.words("english"))



print df['description']


#####Perform basic preprocessing#######

punct = string.punctuation.replace('-', '')

# regex to remove intra-word dashes
my_regex = re.compile(r"(\b[-']\b)|[\W_]")



def clean_string(string):
    
    # remove formatting
    str = re.sub('\s+', ' ', string)
    #lower_case
    str = str.lower()
    #replace dot with space
    str = str.replace('.',' ')
    # remove punctuation (preserving dashes)
    str = ''.join(l for l in str if l not in punct)
    # remove dashes that are not intra-word
    str = my_regex.sub(lambda x: (x.group(1) if x.group(1) else ' '), str)
    # strip extra white space
    str = re.sub(' +',' ',str)
    # strip leading and trailing white space
    str = str.strip()
    #remove digits
    str = str.translate(None, digits) 
    #remove website www and com or couk
    str = re.sub('www', '', str)
    str = re.sub('com','', str)
    str = re.sub('couk','', str)
    #Stem
    #str = stem(str)
    #split words
    str = str.split()
    
    #remove single characters
    str = [element for element in str if len(element)>2]
    return str

clean_string("elelel.dauzdaz.dezbdubau.com")    
    
def clean_string_list(list):
    result = []
    for item in list:
        list_temp = [element for element in clean_string(item)]
        result.extend(list_temp)
    result = filter(None, result)
    return result
    
    


def remove_stopwords(list):
    list = [word for word in list if word not in stpwds]
    return list
    
df['description'] = df['description'].apply(lambda x: make_list(x))
df['description'] = df['description'].apply(lambda x: remove_stopwords(clean_string_list(x)))

print df['description']

#Print top k words
words = df['description'].tolist()
words = [item for sublist in words for item in sublist]
c = Counter(words)
for k, v in c.most_common(100):
    print '%s: %i' % (k, v)

print ('Data size', len(c))


#######Create word embeddings using tensorflow###########
words = df['description'].tolist()
words = [item for sublist in words for item in sublist]


