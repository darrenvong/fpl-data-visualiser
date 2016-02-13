# -*- coding: utf-8 -*-

import urllib2
from urllib2 import URLError, HTTPError
from json import loads
from time import sleep
from collections import OrderedDict
from pymongo import MongoClient

####################### Main scrapping code ###########################

# def checkInactivePlayer(d):
#     return True if d['total_points']==0 else False

def scrapePlayers():
    address = "http://fantasy.premierleague.com/web/api/elements/"
    i = 1
    wtf = open("FPLdata2.json", "w") # wtf = " write to file :) "
    AGENT_NAME = "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0"
    headers = {"User-Agent": AGENT_NAME}
     
    while True:    
        try:
            request = urllib2.Request(address+str(i)+"/", None, headers)
            feed = urllib2.urlopen(request)
            data = feed.read()
        except HTTPError:
            print "All players fetched"
            break
        except URLError:
            print "Dude, turn on the Internet please!"
            sleep(10)
            continue
        try:
            loads(data)
            wtf.write(data+"\n")
            i += 1
        except ValueError:
            print "Invalid JSON, try again!"
        except SyntaxError:
            loads(data,encoding="latin_1")
            i += 1
        
        if (i%50 == 0):
            print "Flushing to file..."
            wtf.flush()
            print data[:30]
            sleep(3)
       
    wtf.close()
    print "... Done"

######################## end of scraping code ############################
def connect():
    client = MongoClient()
    players = client.test.players
    return client, players

def insertPlayers():
    client = MongoClient()
    db = client.test
    players = db.players
    with open("FPLdata.json", "r") as data:
        players_list = [loads(p, object_pairs_hook=OrderedDict) for p in data]
        
    players.insert_many(players_list)
    client.close()

def getPoints(client, players):
    cursor = players.find({"web_name": {"$exists": 1}},
                          {"_id": 0, "web_name": 1, "fixture_history": 1})
    # List of fixtures with players' names
    players_list = [(p["fixture_history"]["all"],p["web_name"]) for p in cursor]
    # Players' scores, weeks they got the scores in together with their names
    players_list = [([f[-1] for f in player[0]], [f[1] for f in player[0]], player[1])
                    for player in players_list]
    return players_list
    