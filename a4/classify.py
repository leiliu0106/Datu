"""
classify.py
"""
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
from TwitterAPI import TwitterAPI
from collections import Counter, defaultdict, deque
import copy
import math
import networkx as nx
import urllib.request
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import re
import nltk
import pickle
import numpy as np

def load_afinn():
    url = urlopen('http://www2.compute.dtu.dk/~faan/data/AFINN.zip')
    zipfile = ZipFile(BytesIO(url.read()))
    afinn_file = zipfile.open('AFINN/AFINN-111.txt')

    afinn = dict()

    for line in afinn_file:
        parts = line.strip().split()
        if len(parts) == 2:
            afinn[parts[0].decode("utf-8")] = int(parts[1])
    return afinn
  
def tokenize(doc, keep_internal_punct=False):
 
    if keep_internal_punct == False:
        res = re.findall('\w+', doc.lower())
    else:
        regex = r'\W+(?!\S*[a-z])|(?<!\S)\W+'
        res = re.sub(regex, '', doc.lower()).split()
    return np.array(res)
    pass
  
def tweet_sentiment(tweet,afinn):
    tokens = tokenize(tweet,keep_internal_punct=False )
    score = 0
    for token in tokens:
        if token in afinn:
            score += afinn[token]
    return score       
  
def tweet_score(all_tweets,afinn):
    l_list = []
    for k,v in all_tweets.items():
        for tweet in v:
            l_list.append((tweet,tweet_sentiment(tweet,afinn)))
    return l_list
  
def tweet_statistics(all_score):
    class_dict = {}
    class_dict['negative'] = 0
    class_dict['positive'] = 0
    class_dict['neutral'] = 0
    for t in all_score:
        if t[1] < 0:
            class_dict['negative'] += 1
        elif t[1] > 0:
            class_dict['positive'] += 1
        else:
            class_dict['neutral'] += 1
    return class_dict
  
def pick_most_tweet(all_score,option):
    lst = sorted(all_score, key = lambda x:x[1])
    if option == 'most positive':
        t = lst[-1][0]
    elif option == 'negative positive':
        t = lst[0][0]
    else:
        l = [i for i in lst if i[1] ==0]
        t = l[0][0]
    return t
  
def main():
    afinn = load_afinn()
    
    print('Open all_tweets files.')
    f = open('all_tweets.pickle', 'rb')
    all_tweets = pickle.load(f)
    f.close()
    f = None
    
    tweet_scores = tweet_score(all_tweets,afinn)
    print('Number of instances per class found:')
    stat_dict = tweet_statistics(tweet_scores)
    print(stat_dict)
    
    print('One example from each class:')
    options = ['most positive','negative positive','neutral']
    example_list = [(option,pick_most_tweet(tweet_scores,option)) for option in options]
    print(example_list)
    
    print('Save class number statistics and three examples.')
    pickle.dump(stat_dict, open('stat_dict.pickle', 'wb'))
    pickle.dump(example_list, open('example_list.pickle', 'wb'))


if __name__ == '__main__':
    main()
