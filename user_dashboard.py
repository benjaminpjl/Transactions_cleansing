#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 14:39:17 2017

@author: benjaminpujol
"""


import numpy as np
import pandas as pd
import os
import nltk
import re
import string
import seaborn as sns
%matplotlib inline
import matplotlib.pyplot as plt
#Change working directory
os.chdir("/Users/benjaminpujol/Documents/Mobillity/Transactions_cleansing")
               
#Pandas options
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 2000)

#Import transactions data 
df = pd.read_csv("data/RAW_TRANSACTION.csv")

#Create a new dataframe where 'description' is lower case
df2 = df.copy(deep=True)
df2['description'] = df2['description'].str.lower()

#Import subscriptions data
colnames = ['name', 'presence', 'keyword', 'type']
sub = pd.read_csv("data/subscriptions.csv", names = colnames, header = None, converters={"keyword": lambda x: x.split("|")})
sub = sub.loc[sub['presence']==1] #Keep only identified subscriptions


### This is a function that allows to look for the subscriptions of one user given is hashed_user_id
def give_subscriptions_user(hash_user_id):
    
    #Dataframe of users transactions
    df_user = df.loc[df['hashed_user_id'] == hash_user_id]
    #Transform description to lower case
    df2_user = df_user.copy(deep=True)
    df2_user['description'] = df2_user['description'].str.lower()
    
    #Add a column 'is_subscription' (is this a subscription for this user) and 'list of transactions indexes' (list of user transactions associated to a subscription)
    sub_user = sub.copy(deep = True)
    sub_user['is_subscription'] = 0
    sub_user['list of transaction indexes'] = np.empty((len(sub_user), 0)).tolist()
  
    #Iterate over subscriptions dataframe
    for i, row in sub_user.iterrows():
    
        #print '|'.join(row['keyword'])
        boolean_subscriptions = df2_user["description"].str.contains('|'.join(row['keyword']))
        list_indexes = df2_user[df2_user["description"].str.contains('|'.join(row['keyword']))].index.tolist()
        
        #print df2_user["description"].str.contains('|'.join(row['keyword']))
        if boolean_subscriptions.any():
            #print "Is a subscription"
            sub_user.ix[i, 'is_subscription'] =  1
            
            sub_user.ix[i, 'list of transaction indexes'].extend(list_indexes)


    result = sub_user.loc[sub_user['is_subscription']==1]
    return result
    
    
def print_subscriptions_user(hash_user_id):
    dict = {}
    df_user = df.loc[df['hashed_user_id'] == hash_user_id]
    subscriptions_user = give_subscriptions_user(hash_user_id)
    for type in subscriptions_user["type"].unique().tolist():
        amount_type = 0
        print "------> ", type.upper(), " <------"
        print "\n"
        for subscription in subscriptions_user.loc[subscriptions_user['type']== type]['name']:
            print subscription, "\n"
            list_indexes =  subscriptions_user.loc[subscriptions_user['name']== subscription]['list of transaction indexes']
            for item in list_indexes:
                print df_user.ix[item][['description', 'amount', 'made_on']].to_string(index = False, header = False)
                print "\n", "Total amount spent on", subscription, "is:", df_user.ix[item]['amount'].sum(axis = 0), "£"
                amount_type += df_user.ix[item]['amount'].sum(axis = 0)
            print "\n"
        print "Total amount spent on", type, amount_type, "£"
        dict[type] = -amount_type
        print "\n"

    #Plot repartition of spendings per type
    
    #Sort dictionary in descending order
    import operator
    sorted_tuples = sorted(dict.items(), key=operator.itemgetter(1), reverse = True)
    print sorted_tuples
    categories= [item[0] for item in sorted_tuples]
    spendings = [item[1] for item in sorted_tuples]
  
    
    #Plotting parameters

    plt.rcParams['figure.figsize']=(20,10)
    fig = sns.barplot(x = categories, y= spendings)  
    fig.set(xlabel = 'Category', ylabel = 'Amount') 
    sns.plt.title("Spendings by category", fontsize = 18)    
    plt.show()
   
    
print give_subscriptions_user('KkmR9ASZHGRvq1ZXP+srWQ==')    
print print_subscriptions_user('GoN/5RvrKovHTIWcZLZPsQ==')


    
