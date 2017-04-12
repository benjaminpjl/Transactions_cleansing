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
colnames = ['name', 'presence', 'keyword', 'type', 'unknown']
sub = pd.read_csv("data/subscriptions.csv", names = colnames, header = None)
del sub['unknown']

#SEARCH FOR A KEYWORD
print df.loc[df2["description"].str.contains('amazon')]['description']

#For each subscriptions print results of the search based on the keyword
for row in sub.itertuples():
    print row[1]
    print df.loc[df2["description"].str.contains(row[3])]['description']
    raw_input('')

    
    


###Statistics on Water###

print "###### Statistics on Water providers ######", '\n'

#print df.loc[df2["description"].str.contains("water")]['description']

water_keywords = {'Thames Water': 'thames water', 'Affinity water': 'affinity water', 'Castle Water': 'castle water'}
number_of_subscribers = {}
list_user_water = []
for key, val in water_keywords.iteritems():
    list_index = df2.loc[df2["description"].str.contains(val)]['hashed_user_id'].tolist()
    list_index = list(set(list_index))
    number_of_subscribers[key] = len(list_index)
    list_user_water.extend(list_index)
    
sorted_subscriptions = sorted(number_of_subscribers.items(), key=lambda x: x[1])[::-1]
for item in sorted_subscriptions:
    print item[0], ":", item[1]  
  
print sorted_subscriptions
print sorted_subscriptions[:][1]
list_user_water = list(set(list_user_water))

print '\n'
print "Number of users that have water bills:", len(list_user_water)
print "Percentage of users:", int(float(len(list_user_water))/float(len(list_of_users))*100),"%", '\n'

sns.countplot(sorted_subscriptions.keys(), sorted_subscriptions.values())

#print "----------- List of users that have water bills ---------------"
#print list(list_user_water)


list_non_water = [item for item in list_of_users if item not in list_user_water]
#print "----------- Number of users that do not have water bills ---------------"
#print len(list_non_water), '\n'

#print "----------- List of users that do not have energy bills ---------------"
#print list_non_water, '\n'


###Statistics on Energy###

print "###### Statistics on Energy providers ######", '\n'

print df.loc[df2["description"].str.contains("t-mobile",re.IGNORECASE)]['description']

energy_keywords = {'EDF':'edf', 'NPower': 'npower', 'E.ON': 'e\.on', 'British Gas': 'gas', 'Scottish Power': 'scottish'}
number_of_subscribers = {}
list_user_energy = []
for key, val in energy_keywords.iteritems():
    list_index = df2.loc[df2["description"].str.contains(val)]['hashed_user_id'].tolist()
    list_index = list(set(list_index))
    number_of_subscribers[key] = len(list_index)
    list_user_energy.extend(list_index)         

sorted_subscriptions = sorted(number_of_subscribers.items(), key=lambda x: x[1])[::-1]
for item in sorted_subscriptions:
    print item[0], ":", item[1]     

    
list_user_energy= list(set(list_user_energy))

print '\n'
print "Number of users that have energy bills:", len(list_user_energy)
print "Percentage of users:", int(float(len(list_user_energy))/float(len(list_of_users))*100),"%", '\n'

#print "----------- List of users that have energy bills ---------------"
#print list_user_energy, '\n'


#list_non_energy = [item for item in list_of_users if item not in list_user_energy]
#print "Number of users that do not have energy bills:"
#print len(list_non_energy), '\n'

#print "----------- List of users that do not have energy bills ---------------"
#print list_non_energy, '\n'

###Statistics on Mobile Phone providers###

print "###### Statistics on Mobile Phone providers ######", '\n', '\n'

#print df.loc[df2["description"].str.contains("ee")]['description']
mobile_keywords = {'EE T-mobile':'t-mobile', 'Virgin Mobile': 'virgin mobile', 'Three': 'h3g', 'GIFFGAFF': 'giffgaff', 'Talk talk': 'talktalk', 'Vodafone': 'vodafone'}
number_of_subscribers = {}
list_user_mobile = []
for key, val in mobile_keywords.iteritems():
    list_index = df2.loc[df2["description"].str.contains(val)]['hashed_user_id'].tolist()
    list_index = list(set(list_index))
    number_of_subscribers[key] = len(list_index)
    list_user_mobile.extend(list_index)              

    
sorted_subscriptions = sorted(number_of_subscribers.items(), key=lambda x: x[1])[::-1]
for item in sorted_subscriptions:
    print item[0], ":", item[1]
           
list_user_mobile = list(set(list_user_mobile))

print '\n'
print "Number of users that have mobile bills:", len(list_user_mobile)
print "Percentage of users:", int(float(len(list_user_mobile))/float(len(list_of_users))*100),"%", '\n'


#print "----------- List of users that have mobile bills ---------------"
#print list(list_user_mobile)


list_non_mobile = [item for item in list_of_users if item not in list_user_mobile]
#print "----------- Number of users that do not have mobile bills ---------------"
#print len(list_non_mobile), '\n'

#print "----------- List of users that do not have mobile bills ---------------"
#print list_non_mobile, '\n'



###Statistics on Broadband providers###

print "###### Statistics on Broadband and TV providers ######", '\n', '\n'

#print df.loc[df2["description"].str.contains("tv licence")]['description']
broadband_keywords = {'Sky Digital': 'sky digital', 'Virgin Media': 'virgin media', 'Netflix': 'netflix', 'Tvlicensing.co': 'tvlicensing', 'TV licence MBP': 'tv licence'}
number_of_subscribers = {}
list_user_broadband = []
for key, val in broadband_keywords.iteritems():
    list_index = df2.loc[df2["description"].str.contains(val)]['hashed_user_id'].tolist()
    list_index = list(set(list_index))
    number_of_subscribers[key] = len(list_index)
    list_user_broadband.extend(list_index)     

sorted_subscriptions = sorted(number_of_subscribers.items(), key=lambda x: x[1])[::-1]
for item in sorted_subscriptions:
    print item[0], ":", item[1]
           
        
list_user_broadband = list(set(list_user_broadband))

print '\n'
print "Number of users that have broadband bills:", len(list_user_broadband)
print "Percentage of users:", int(float(len(list_user_broadband))/float(len(list_of_users))*100),"%", '\n'

#print "----------- List of users that have broadband bills ---------------"
#print list(list_user_broadband)

#print "----------- Number of users that do not have broadband bills -------------"
#print len(list_non_broadband), '\n'

#print "----------- List of users that do not have broadband bills ---------------"
#print list_non_broadband, '\n'