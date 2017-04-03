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

#Change working directory
os.chdir("/Users/benjaminpujol/Documents/Mobillity/Transactions_cleansing")


#Import data 
df = pd.read_csv("data/SORTED_BILL.csv")
print df.head(5)


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


##Perform basic preprocessing

punct = string.punctuation.replace('-', '')

# regex to remove intra-word dashes
my_regex = re.compile(r"(\b[-']\b)|[\W_]")

def clean_string(string):
    # remove formatting
    str = re.sub('\s+', ' ', string)
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
    #lower_case
    str = str.lower()
    return str
    
def clean_string_list(list):
    list = [clean_string(word) for word in list]
    list = filter(None, list)
    return list
    
def remove_stopwords(list):
    list = [word for word in list if word not in stpwds]
    return list
    
df['description'] = df['description'].apply(lambda x: make_list(x))
df['description'] = df['description'].apply(lambda x: remove_stopwords(clean_string_list(x)))

print df['description']

df['description'].to_csv("test.csv", sep=',')