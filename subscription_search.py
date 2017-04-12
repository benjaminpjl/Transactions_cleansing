#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 13:47:40 2017

@author: benjaminpujol
"""

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
import collections
from collections import Counter
from nltk.tokenize import word_tokenize
from configuration import CONFIG
import gensim
import random
import tensorflow as tf
import math

#Pandas options
pd.set_option('display.max_rows', 500)

#Change working directory
os.chdir("/Users/benjaminpujol/Documents/Mobillity/Transactions_cleansing")


#Import data 
df = pd.read_csv("data/RAW_TRANSACTION.csv")



#Tokenize description

def make_list(row):
    row = nltk.word_tokenize(row)
    return(row) #unique elements

def take_first(row): 
    return row.pop(0)

#Set stopwords
nltk.download('stopwords')
stpwds = set(nltk.corpus.stopwords.words("english"))



#####Perform basic preprocessing#######

punct = string.punctuation.replace('-', '')

# regex to remove intra-word dashes
my_regex = re.compile(r"(\b[-']\b)|[\W_]")


#Remove digits if more than 1 digits
def more_than_two_numbers(string):
   numbers = sum(c.isdigit() for c in string)
   if numbers>1:
       return ''
   else:
       return string
       

   

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
    #remove website www and com or couk
    str = re.sub('www', '', str)
    str = re.sub('com','', str)
    str = re.sub('couk','', str)
    #Stem
    #str = stem(str)
    #split words
    str = str.split()
    
    #remove words in custom list
    str = [element for element in str if element not in CONFIG.useless_words.values()]    
    #remove words with more than one digit inside
    str = [more_than_two_numbers(element) for element in str]

    #remove words that are less than 2 characters
    str = [element for element in str if len(element)>2]
    #Keep only one occurence of each word
    str = list(set(str))      
    
    return str
    
    
print CONFIG.useless_words.values()
    

  
    
 
    
def clean_string_list(list):
    result = []
    for item in list:
        list_temp = [element for element in clean_string(item)]
        result.extend(list_temp)
    return result
    
    


def remove_stopwords(liste):
    liste = [word for word in liste if word not in stpwds]
    return list(set(liste))
    
df['description'] = df['description'].apply(lambda x: make_list(x))
df['description'] = df['description'].apply(lambda x: remove_stopwords(clean_string_list(x)))

#search for subscription 
def search_subscription(substring):
    df_temp = df.loc[df['description'].map(lambda x: substring in x)]
    return df_temp["description"]
                  
print search_subscription("edf")
