"""
sumarize.py
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

def main():
    text_file = open('summarize.txt', 'w', encoding = 'utf-8')
    
    print('open users file.')
    f1 = open('users.pickle', 'rb')
    users = pickle.load(f1)
    f1.close()
    f1= None
    
    print('Open all_tweets files.')
    f2 = open('all_tweets.pickle', 'rb')
    all_tweets = pickle.load(f2)
    f2.close()
    f2 = None
    
    print('open subs file.')
    f3 = open('subs.pickle', 'rb')
    subs = pickle.load(f3)
    f3.close()
    f3= None
    
    print('open stat_dict file.')
    f4 = open('stat_dict.pickle', 'rb')
    stat_dict = pickle.load(f4)
    f4.close()
    f4= None
    
    print('open example_list file.')
    f5 = open('example_list.pickle', 'rb')
    example_list = pickle.load(f5)
    f5.close()
    f5= None
    
    print('open graph file.')
    f6 = open('graph.pickle', 'rb')
    graph = pickle.load(f6)
    f6.close()
    f6= None

    text_file.write('Number of {0} users collected and their screen name:\n{1}'.format(len(users), str([u['screen_name'] for u in users])))
    

    text_file.write('\n')
    text_file.write('Number of {0} messages collected'.format(sum([len(v) for v in all_tweets.values()])))
                   
    text_file.write('\n')
    text_file.write('Number of {0} communities discovered'.format(len(subs)))

    text_file.write('\n')
    text_file.write('Average number {0} of users per community'.format((len(graph.nodes())/len(subs))))
    
    text_file.write('\n')
    text_file.write('Actual number {0} of users per community'.format(([len(sub) for sub in subs])))
                    
    text_file.write('\n')
    text_file.write('{0} number of instances per class found'.format((stat_dict)))
    
    text_file.write('\n')
    text_file.write('One example from each class{0}'.format((example_list)))
    text_file.write('\n')
    text_file.write('Check each user belongs to which community:')
    text_file.write('\n')
    
    idName = {}
    for u in users:
        idName[u['id']] = u['screen_name']

    for sub in subs:
        text_file.write(str(len(sub)))
        text_file.write('\n')
        for one in sub:
            if one in idName:
                text_file.write(idName[one])
                text_file.write('\n')
        text_file.write('-----------')
        text_file.write('\n')

if __name__ == '__main__':
    main()

