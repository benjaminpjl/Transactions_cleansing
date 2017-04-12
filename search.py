#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 14:46:56 2017

@author: benjaminpujol
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
pd.set_option('display.width', 2000)

#Change working directory
os.chdir("/Users/benjaminpujol/Documents/Mobillity/Transactions_cleansing")


#Import data 
df = pd.read_csv("data/RAW_TRANSACTION.csv")

list_of_users =  df['hashed_user_id'].unique()
df2 = df.copy(deep=True)
df2['description'] = df2['description'].str.lower()

list_index=  df2.loc[df2["description"].str.contains("thames water")].index.tolist()
df_search = df2.loc[df2["description"].str.contains("water")]

                    
list_user_water = []
for index in list_index:
    print df.loc[index]['hashed_user_id']
    print df.loc[index]['description']
    list_user_water.append(df.loc[index]['hashed_user_id'])
     
    
list_user_water = list(set(list_user_water))

list_non_water = [item for item in list_of_users if item not in list_user_water]
print list_non_water
print len(list_non_water)
    
#9 Thames Water
#1 Castle Water
#1 Affinity Water