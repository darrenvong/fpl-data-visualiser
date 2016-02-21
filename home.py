"""
Created on 21 Feb 2016

@author: Darren
"""
from pymongo import MongoClient
import pymongo

def connect():
    client = MongoClient()
    players = client.players.current_gw
    return client, players

def get_hot_players(col):
    query = {"total_points": {"$gt": 0}}
    projection = {"_id": 0, "web_name": 1, "team_name": 1, "now_cost": 1, "total_points": 1}
    cursor = col.find(query, projection, sort=[("form", pymongo.DESCENDING)], limit=5)
    return [player for player in cursor]

def pound_stretchers(col):
    pass

_, players = connect()
players_list = get_hot_players(players)
print players_list