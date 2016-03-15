# -*- coding: utf-8 -*-

"""
@author: Darren
"""

from pymongo import MongoClient, UpdateMany
from collections import OrderedDict
from accent_fold import accent_fold

# idea adapted from Pringle's (2014) code
FIXTURE_KEY_MAP = {
    0 : "date", 
    1 : "gameweek",
    2 : "opponent_result", 
    3 : "mins_played", 
    4 : "goals_scored",
    5 : "assists",
    6 : "clean_sheet",
    7 : "goals_conceded",
    8 : "own_goals",
    9 : "pens_saved",
    10 : "pens_missed",
    11 : "yellow_cards",
    12 : "red_cards",
    13 : "saves",
    14 : "bonus_points",
    15 : "ea_sports_ppi",
    16 : "bonus_point_system",
    17 : "net_transfers",
    18 : "value",
    19 : "points"
}

def connect():
    client = MongoClient()
    players = client.players.current_gw
    return client, players

def restructure_data(col):
    query = {}
    projection = {"_id": 0, "web_name": 1, "fixture_history": 1}
    cursor = col.find(query, projection)
    fix_hist_list = [OrderedDict(name=history["web_name"],
                        fixture_history=history["fixture_history"]["all"]) for history in cursor]
    for fixture_list in fix_hist_list: # fixture_list = dictionary with name and fixture history
        fixture_objects_list = []
        # goes through each fixture and convert to objects
        for fixture in fixture_list["fixture_history"]:
            fixture_object = OrderedDict()
            for i in xrange(20):
                fixture_object[FIXTURE_KEY_MAP[i]] = fixture[i]
            fixture_objects_list.append(fixture_object)
        fixture_list["fixture_history"] = fixture_objects_list
    return fix_hist_list

def update_db(col, fix_hist_list):
    counter = 0
    for fixture_list in fix_hist_list:
        query = {"web_name": fixture_list["name"]}
        update = {"$set": {"fixture_history": fixture_list["fixture_history"]}}
        result = col.update_one(query, update)
        counter += result.modified_count
    print str(counter)+" affected!"
    
def normalise_names(col):
    cursor = col.find({}, {"_id": 0, "web_name": 1})
    player_names = [player_obj["web_name"] for player_obj in cursor]
    normalised = [accent_fold(name).capitalize() for name in player_names]
    updates = [UpdateMany({"web_name": name}, {"$set": {"normalised_name": normalised[i]}})
                for i, name in enumerate(player_names)]
    result = col.bulk_write(updates)
    print result.inserted_count, result.modified_count

if __name__ == '__main__':
    c, col = connect()
    normalise_names(col)