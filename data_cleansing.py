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
print df 
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

print df['description'].head(500)

#
#
########Create word embeddings using tensorflow###########
#
#vocabulary_size = 2000
#
##Create a list of vocabulary
#words = df['description'].tolist()
#words = [item for sublist in words for item in sublist]
#print "Data size", len(words)
#
##Build a dictionary and replace rare words with UNK token
#
#def build_dataset(words):
#    count = [['UNK', -1]]
#    count.extend(Counter(words).most_common(vocabulary_size-1))
#    dictionary = dict()
#    for word,_ in count:
#        dictionary[word]= len(dictionary)
#    data = list()
#    unk_count = 0
#    for word in words:
#        if word in dictionary:
#            index = dictionary[word]
#        else:
#            index = 0 ##dictionary["UNK"]
#            unk_count +=1
#        data.append(index)
#    count[0][1]=unk_count
#    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
#    return data, count, dictionary, reverse_dictionary
#
#    
#data, count, dictionary, reverse_dictionary = build_dataset(words)
#
#print reverse_dictionary
#
#
##Create a function to generate a training batch for the skip-gram model
#data_index = 0
#
#def generate_batch(batch_size, num_skips, skip_window):
#    global data_index
#    assert batch_size % num_skips == 0
#    assert num_skips <= 2*skip_window
#    batch = np.ndarray(shape=(batch_size), dtype=np.int32)
#    labels = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
#    span = 2 * skip_window + 1  # [ skip_window target skip_window ]
#    buffer = collections.deque(maxlen=span)
#    for _ in range(span):
#        buffer.append(data[data_index])
#        data_index = (data_index + 1) % len(data)
#        
#    for i in range(batch_size // num_skips):
#        target = skip_window  # target label at the center of the buffer
#        targets_to_avoid = [skip_window]
#        for j in range(num_skips):
#            while target in targets_to_avoid:
#                target = random.randint(0, span - 1)
#            targets_to_avoid.append(target)
#            batch[i * num_skips + j] = buffer[skip_window]
#            labels[i * num_skips + j, 0] = buffer[target]
#        buffer.append(data[data_index])
#        data_index = (data_index + 1) % len(data)
#    return batch,labels
#  
#  
#batch, labels = generate_batch(batch_size=8, num_skips=2, skip_window=1)
#for i in range(8):
#  print(batch[i], reverse_dictionary[batch[i]],
#        '->', labels[i, 0], reverse_dictionary[labels[i, 0]])
#
##### Build and train a skip-gram model.
#
#batch_size = 128
#embedding_size = 128  # Dimension of the embedding vector.
#skip_window = 1       # How many words to consider left and right.
#num_skips = 2         # How many times to reuse an input to generate a label.
#
## We pick a random validation set to sample nearest neighbors. Here we limit the
## validation samples to the words that have a low numeric ID, which by
## construction are also the most frequent.
#valid_size = 16     # Random set of words to evaluate similarity on.
#valid_window = 100  # Only pick dev samples in the head of the distribution.
#valid_examples = np.random.choice(valid_window, valid_size, replace=False)
#num_sampled = 64    # Number of negative examples to sample.
#
#graph = tf.Graph()
#
#with graph.as_default():
#    # Input data.
#  train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
#  train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
#  valid_dataset = tf.constant(valid_examples, dtype=tf.int32)
#
#  # Ops and variables pinned to the CPU because of missing GPU implementation
#  with tf.device('/cpu:0'):
#    # Look up embeddings for inputs.
#    embeddings = tf.Variable(
#        tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))
#    embed = tf.nn.embedding_lookup(embeddings, train_inputs)
#
#    # Construct the variables for the NCE loss
#    nce_weights = tf.Variable(
#        tf.truncated_normal([vocabulary_size, embedding_size],
#                            stddev=1.0 / math.sqrt(embedding_size)))
#    nce_biases = tf.Variable(tf.zeros([vocabulary_size]))
#
#  # Compute the average NCE loss for the batch.
#  # tf.nce_loss automatically draws a new sample of the negative labels each
#  # time we evaluate the loss.
#  loss = tf.reduce_mean(
#      tf.nn.nce_loss(weights=nce_weights,
#                     biases=nce_biases,
#                     labels=train_labels,
#                     inputs=embed,
#                     num_sampled=num_sampled,
#                     num_classes=vocabulary_size))
#
#  # Construct the SGD optimizer using a learning rate of 1.0.
#  optimizer = tf.train.GradientDescentOptimizer(1.0).minimize(loss)
#
#  # Compute the cosine similarity between minibatch examples and all embeddings.
#  norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
#  normalized_embeddings = embeddings / norm
#  valid_embeddings = tf.nn.embedding_lookup(
#      normalized_embeddings, valid_dataset)
#  similarity = tf.matmul(
#      valid_embeddings, normalized_embeddings, transpose_b=True)
#
#  # Add variable initializer.
#  init = tf.global_variables_initializer()
#
#  # Step 5: Begin training.
#num_steps = 100001
#
#with tf.Session(graph=graph) as session:
#  # We must initialize all variables before we use them.
#  init.run()
#  print("Initialized")
#
#  average_loss = 0
#  for step in xrange(num_steps):
#    batch_inputs, batch_labels = generate_batch(
#        batch_size, num_skips, skip_window)
#    feed_dict = {train_inputs: batch_inputs, train_labels: batch_labels}
#
#    # We perform one update step by evaluating the optimizer op (including it
#    # in the list of returned values for session.run()
#    _, loss_val = session.run([optimizer, loss], feed_dict=feed_dict)
#    average_loss += loss_val
#
#    if step % 2000 == 0:
#      if step > 0:
#        average_loss /= 2000
#      # The average loss is an estimate of the loss over the last 2000 batches.
#      print("Average loss at step ", step, ": ", average_loss)
#      average_loss = 0
#
#    # Note that this is expensive (~20% slowdown if computed every 500 steps)
##    if step % 10000 == 0:
##      sim = similarity.eval()
##      for i in xrange(valid_size):
##        valid_word = reverse_dictionary[valid_examples[i]]
##        top_k = 8  # number of nearest neighbors
##        nearest = (-sim[i, :]).argsort()[1:top_k + 1]
##        log_str = "Nearest to %s:" % valid_word
##        for k in xrange(top_k):
##          close_word = reverse_dictionary[nearest[k]]
##          log_str = "%s %s," % (log_str, close_word)
##        print(log_str)
#  final_embeddings = normalized_embeddings.eval()
#
#  
#def plot_with_labels(low_dim_embs, labels, filename='tsne.png'):
#  assert low_dim_embs.shape[0] >= len(labels), "More labels than embeddings"
#  plt.figure(figsize=(18, 18))  # in inches
#  for i, label in enumerate(labels):
#    x, y = low_dim_embs[i, :]
#    plt.scatter(x, y)
#    plt.annotate(label,
#                 xy=(x, y),
#                 xytext=(5, 2),
#                 textcoords='offset points',
#                 ha='right',
#                 va='bottom')
#
#  plt.savefig("word_embeddings.pdf")
#
#try:
#  from sklearn.manifold import TSNE
#  import matplotlib.pyplot as plt
#
#  tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
#  plot_only = 500
#  low_dim_embs = tsne.fit_transform(final_embeddings[:plot_only, :])
#  labels = [reverse_dictionary[i] for i in range(plot_only)]
#  plot_with_labels(low_dim_embs, labels)
#
#except ImportError:
#  print("Please install sklearn, matplotlib, and scipy to visualize embeddings.")
#
#
#
