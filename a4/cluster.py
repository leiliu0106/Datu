"""
cluster.py
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

def print_num_friends(users):
    for user in users:
        print(user['screen_name'], len(user['friends']))
        
def count_friends(users):
    c = Counter()
    for user in users:
        c.update(user['friends'])
    return c
    pass



def create_graph(users, friend_counts):
    
    graph = nx.Graph()
    for user in users:
        for id in user['friends']:
            if friend_counts[id] > 1:
                graph.add_edge(id, user['id'])
    return graph
    pass


def draw_network(graph, users, filename):
   
    labeldict = {}
    for i in users:
        labeldict[i['id']] = i['screen_name']
    
    nx.draw(graph,labels=labeldict, with_labels = True,node_size=50,font_size=22,edge_color='b',node_color='y', alpha=0.8)
    plt.show()
    plt.savefig(filename)
    pass
  
def girvan_newman(graph):
    comp = nx.algorithms.community.centrality.girvan_newman(graph)
    subs = None
    for subs in comp:
        if len(subs) > 2:
            break
    return subs
  
def main():
    
    print('open users file.')
    f = open('users.pickle', 'rb')
    users = pickle.load(f)
    f.close()
    f= None
    
    
    print('Friends per user:')
    print_num_friends(users)
    print('----------------------------------------')
   
    friend_counts = count_friends(users)
    graph = create_graph(users, friend_counts)
   
    print('node number and edges number:',(len(graph.nodes()), len(graph.edges())))
    print('Use girvan_newman to find community:')
    subs = girvan_newman(graph)
    print('Number of communities discovered:',len(subs))
    print('Average number of users per community:',len(graph.nodes())/len(subs))
    print('Actual number of users per community:',[len(sub) for sub in subs])
    
    print('Save the communities.')
    pickle.dump(subs, open('graph.pickle', 'wb'))
    pickle.dump(subs, open('subs.pickle', 'wb'))
    

if __name__ == '__main__':
    main()
