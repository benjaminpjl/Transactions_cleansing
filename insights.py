#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 16:31:22 2017

@author: benjaminpujol
"""

import numpy as np
import pandas as pd
import os
import time
dateparse = lambda x: time.strptime(x, '%Y-%m-%d')



#Change working directory
os.chdir("/Users/benjaminpujol/Documents/Mobillity/Transactions_cleansing")


#Import data 
df = pd.read_csv("data/RAW_TRANSACTION.csv")
print df.head(5)

#Convert date from a string to a datetime format
df["made_on"] = df["made_on"].apply(dateparse)

#Create features 'month', 'year'
df['year'] = df['made_on'].apply(lambda x: x.tm_year)
   
df['month'] = df['made_on'].apply(lambda x: x.tm_mon)




#Group by users
df1 = df.groupby(["hashed_user_id"]).size().reset_index(name='Size')

average_number_transactions = df1["Size"].mean(axis=0)
number_of_users = len(df1.index)
print "average number of transactions per user -->", average_number_transactions
print"number of users -->", number_of_users


#Group by users and months and years
df2 = df.groupby(["month", "year"]).size().reset_index(name="Size")
print df2
df3  = df2.groupby(["month", "year"]).count()
print df3
