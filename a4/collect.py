"""
collect.py
"""
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
from TwitterAPI import TwitterAPI
import matplotlib.pyplot as plt
import pickle

consumer_key = 'uzwazJyR1BS3bJFd41jU8We5n'
consumer_secret = 'hC0GRtw9wOnZtDMq1DcghxtSSRUVda7WJhO0RTQN9iWHv9mox1'
access_token = '769992044269936641-NBiMKReF0KL7M81V9AxJkhJHDDEMnMG'
access_token_secret = 'n18dd6cGogwvK3lgjkeg4ZBXWWGqFL5LPn1YrbKvDlEMR'

def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)
  
def robust_request(twitter, resource, params, max_tries=5):
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)
            
def read_screen_names(filename):
    f = open(filename)
    content = [x.strip() for x in f.readlines()]
    f.close()
    return content

def get_users(twitter, screen_names):
   
    request = robust_request(twitter,'users/lookup',{'screen_name' : ','.join(screen_names)})
    users = [r for r in request]
    return sorted(users, key=lambda x: x['screen_name'])

def get_friends(twitter, screen_name):
   
    request = robust_request(twitter,'friends/ids', {'screen_name':screen_name})
    friends = [r for r in request]
    return sorted(friends)

def add_all_friends(twitter, users):
    
    for user in users:
        friends = get_friends(twitter, user['screen_name'])
        user['friends'] = friends
        
        
def get_tweets(twitter, screen_names):
    tweet_dict = {}
    for screen_name in screen_names:
        request = robust_request(twitter, 'search/tweets', {'q': screen_name, 'count': 100})
        tweets = [t['text'] for t in request]
        tweet_dict[screen_name] = tweets

    return tweet_dict
  
def main():
 
    twitter = get_twitter()
    print('Read user names.')
    screen_names = read_screen_names('tweet_account.txt')
    
    users = get_users(twitter, screen_names)
    add_all_friends(twitter, users)
    print('Number of users collected and their screen names:', (len(users), str([u['screen_name'] for u in users])))
    print('Save users.')
    pickle.dump(users, open('users.pickle', 'wb'))

    print('Save all tweets for all users.')
    all_tweets = get_tweets(twitter, screen_names)
    pickle.dump(all_tweets, open('all_tweets.pickle', 'wb'))
    print('Number of messages collected' ,sum([len(v) for v in all_tweets.values()]))


if __name__ == '__main__':
    main()
