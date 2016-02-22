"""
Created on 21 Feb 2016

@author: Darren
"""
from pymongo import MongoClient, DESCENDING
from bson import SON

def connect():
    client = MongoClient()
    players = client.players.current_gw
    return client, players

def get_hot_players(col):
    query = {"total_points": {"$gt": 0}}
    projection = {"_id": 0, "web_name": 1, "team_name": 1, "now_cost": 1, "total_points": 1,
                  "form": 1}
    cursor = col.find(query, projection, sort=[("form", DESCENDING)], limit=5)
    return [player for player in cursor]

def pound_stretchers(col):
    avg_points = round(find_key_averages(col))
    avg_cost = 50
    query = {"now_cost": {"$lte": avg_cost}, "total_points": {"$gte": avg_points}}
    projection = {"_id": 0, "web_name": 1, "team_name": 1, "now_cost": 1, "total_points": 1}
    cursor = col.find(query, projection, sort=[("total_points", DESCENDING)], limit=5)
    return [player for player in cursor]
        
def find_key_averages(col):
    """Finds the average points and values of all active players in Fantasy Premier League"""
    query = {"total_points": {"$gt": 0}}
    projection = {"_id": 0, "avg_points": 1}
    pipeline = [{"$match": query}, {"$group": {"_id": None, "avg_points": {"$avg": "$total_points"}}},
                {"$project": projection}]
    cursor = col.aggregate(pipeline)
    return cursor.next()["avg_points"]

def most_popular(col):
    projection = {"_id": 0, "web_name": 1, "team_name": 1, "now_cost": 1, "total_points": 1,
                  "net_transfers": {"$subtract": ["$transfers_in_event", "$transfers_out_event"]}}
    pipeline = [{"$project": projection}, {"$sort": SON([("net_transfers", -1)])},
                {"$limit": 5}]
    cursor = col.aggregate(pipeline)
    return [player for player in cursor]

if __name__ == "__main__":
    _, players = connect()
    hot, ps, mp = get_hot_players(players), pound_stretchers(players), most_popular(players)
    print hot
    print ps
    for p in mp:
        print p["web_name"], p["net_transfers"]
    