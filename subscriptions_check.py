#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 10:40:19 2017

@author: benjaminpujol
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 11:59:19 2017

@author: benjaminpujol
"""

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
import seaborn as sns
%matplotlib inline
import matplotlib.pyplot as plt

#Pandas options
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 2000)

#Change working directory
os.chdir("/Users/benjaminpujol/Documents/Mobillity/Transactions_cleansing")


#Import transactions data 
df = pd.read_csv("data/RAW_TRANSACTION.csv")

#Transform description to lower case
df2 = df.copy(deep=True)
df2['description'] = df2['description'].str.lower()

#Import subscriptions data
colnames = ['name', 'presence', 'keyword', 'type']
sub = pd.read_csv("data/subscriptions.csv", names = colnames, header = None, converters={"keyword": lambda x: x.split("|")})

# Add a column for number of users 
  

sub = sub.loc[sub['presence']==1]

#SEARCH FOR A KEYWORD
#print df.loc[df2["description"].str.contains('co-op')]['description']
#Search for a particular subscription
#keywords=  ["southern electric", "se gas"]
#df.loc[df2["description"].str.contains('|'.join(keywords))]['description']         

        


#For each subscriptions print results of the search based on the keyword
#This function is used to check the quality of the keywords

def print_subscriptions(data):
    
    for i, row in data.iterrows():
        print i 
        print row['keyword']
        print '|'.join(row['keyword'])
        result = df.loc[df2["description"].str.contains('|'.join(row['keyword']))]
        print result['description']
        raw_input('') #press key to change subscription
    
    
#This function adds a column "number_of_users" to the subscription dataframe
#It is the number of users for a given subscription
def number_users_per_subscription(data):
    
    data['number_of_users'] = 0 
    for i, row in data.iterrows():
        number_of_users = 0
        result = df.loc[df2["description"].str.contains('|'.join(row['keyword']))]
        number_of_users = len(result['hashed_user_id'].unique())
        data.ix[i, 'number_of_users'] =  number_of_users
    return sub
    
#This function adds a column "list_of_users" to the subscription dataframe
#It is the list of "hashed_user_id" that are subscribed to this subscription
def list_users_per_subscription(data):
    
    data['list of users'] = np.empty((len(sub), 0)).tolist()
    for i, row in data.iterrows():
        result = df.loc[df2["description"].str.contains('|'.join(row['keyword']))]
        indexes = result.index.tolist()
        users = df.ix[indexes]["hashed_user_id"].unique()
        data.ix[i, 'list of users'].extend(users)
        
    return sub
    

#Add number of users
sub = number_users_per_subscription(sub)

#Add list of users
sub = list_users_per_subscription(sub)
print sub

#This function return the list of users that are subscribed to a particular subscription
def print_users_for_subscription(subscription):
    users = sub.loc[sub['name'] == subscription]["list of users"].tolist()[0]
    print "The list of users subscribed to", subscription, "is:", users

#print_users_for_subscription('Amazon')



######GLOBAL DASHBOARD#######

#Plotting parameters

plt.rcParams['figure.figsize']=(20,10)

#List of types to plot in the dashboard
types = ["energy", "water", "broadband", "mobile", "bank" ]

###Plotting number of users for energy providers###

def plot_dashboard(types):
    for category in types:
        plt.figure()
        sub_plot = sub.loc[sub['type']==category]
        sub_plot = sub_plot.sort(columns = 'number_of_users', ascending = False)
        data_plot = sub_plot[['name', 'number_of_users']]


        fig = sns.barplot(x = "name", y= 'number_of_users', data = data_plot)  
        fig.set(xlabel = 'Provider', ylabel = 'Number of Mobillity users')
        sns.plt.title(category.upper(), fontsize = 18)    
        plt.show()

plot_dashboard(types)