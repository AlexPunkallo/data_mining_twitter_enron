
# coding: utf-8

# (a) First download at least 10,000 tweets, related to some popular keyword (e.g., immigration), using the search API.

        # Preparing to collect the informations from twitter

import tweepy
from tweepy import OAuthHandler
import time
import networkx as nx
import sys
import pymongo
import networkx as nx
from networkx import degree_centrality, closeness_centrality
import matplotlib.pyplot as plt

def request(keys):
    auth = OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
    auth.set_access_token(keys["access_token"], keys["access_token_secret"])
    api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api 
 
cfg = { 
    "consumer_key"        : "O6JI5GoXF6UeYEE03yYsOX5c0",
    "consumer_secret"     : "o1HDzZQvP65UdZBS47A3wb37p8DMJV4MJ9mDVqrWJ6LNq5FB54",
    "access_token"        : "460537861-e8EDEZCkiOuuhSvBXESMVIC4SPxM8Ksu3Z4wKABJ",
    "access_token_secret" : "gsNC1eCHK6eSvJ3DzrOao66odJXURGQ43aNerPDpmtVpH" 
    }
api=request(cfg)

        # Collecting tweets informations

def dwn_tweets(max_t,qry):
    searched_tweets = []
    last_id = -1
    while len(searched_tweets) < max_t:
        count = max_t - len(searched_tweets)
        try:
            new_tweets = api.search(q=qry, count=count, max_id=str(last_id - 1))
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            break
    return searched_tweets

query = 'etruria'
max_tweets = 1  
searched_tweets=dwn_tweets(max_tweets, query)

# (b) Obtain the followers of the users who tweeted. Note that you need to wait quite some time for this part.

        # Obtain the ids of the tweets
    
def tw_id_fun(s_t):
    tweets_id=[]
    for i in range(len(s_t)):
        tweets_id.append(s_t[i].user.id)
    return tweets_id

tweets_id=tw_id_fun(searched_tweets)

        # Obtain the ids of the followers (computed directly in the (c) point storing them for the graph)

def followers_fun(t_i):
    followers=[]
    for page in tweepy.Cursor(api.followers_ids, id=t_i).pages():
        followers.extend(page)
    return followers

# (c) Store the information of the tweets and of the graph into MongoDB.

        # Preparing the database on MongoDB

MONGODB_URI='mongodb://alexpunkallo:alexpunkallo@ds033875.mongolab.com:33875/twitter_database'
client = pymongo.MongoClient(MONGODB_URI)
db = client.get_default_database()    
       
        # Storing tweets information

def create_dic(s_t):
    dic={}
    list_dic=[]
    for i in s_t:
        dic["ID_Tweet"]=i.id
        dic["Text"]=i.text
        dic["ID_Tweeter"]=i.author.id
        dic["Nickname"]=i.author.screen_name
        dic["Name"]=i.author.name
        list_dic.append(dic.copy())
    return list_dic

list_dic=create_dic(searched_tweets)
lista_db=db['tweets_info']
lista_db.insert(list_dic)

        # Storing graph informations

followers_db=db['followers']

for tweet in tweets_id:
    if followers_db.find({'user':tweet}).count()==0:
        followers=followers_fun(tweet)
        followers_db.insert({ 'author': tweet, 'followers': followers})
    else:
        continue

# (c) Create the graph of the users and perform the operations you did in the first part

        # Create two lists of tweets and followers ids

def lists_fun(curs):
    list1=[]
    list2=[]
    for doc in curs:
        doc1=doc['author']
        doc2=doc['followers']
        list1.append(doc1)
        list2.append(doc2)
    return list1, list2

(list1,list2)=lists_fun(followers_db.find())

#cursor = followers_db.find()      # <---- Use these commands to try with some nodes
#cursor1=cursor[0:500]
#(list1,list2)=lists_fun(cursor1)

        # Create the graph with the lists

def links_fun(t_i,foll):
    links=[]
    for i in range(len(t_i)):
        for j in range(len(foll[i])):
            links.append((t_i[i],foll[i][j]))
    return links
links=links_fun(list1, list2)

        # Compute the degree distribution

graph = nx.Graph()
graph.add_edges_from(links)

def degree_distribution():
    dic = {}
    for n in graph.nodes():
        d = graph.degree(n)
        if d not in dic:
            dic[d] = 0
        dic[d] += 1
    items = sorted (dic.items())
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter([x for (x ,y) in items] ,[y for (x, y) in items])
    ax.set_xscale ('log')
    ax.set_yscale ('log')
    plt.title ("Enron Dataset Distribution")
    fig.savefig ("degree_distribution.png")
    plt.show()
degree_distribution()

# Performing the same operations made with Enron

deg_cen=nx.degree_centrality(graph)
cl_cen=nx.closeness_centrality(graph)
bet_cen=nx.betweenness_centrality(graph)
page_rank=nx.pagerank(graph, alpha=0.9)
#graph=graph.to_undirected()
clust=nx.clustering(graph)
con_comp=nx.connected_components(graph)
k_core=nx.k_core(graph)

# (Not required: draw graph)

#nx.draw(graph)
#plt.savefig("graph.png")

