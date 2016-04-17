# -*- coding: utf-8 -*-

"""
@author: Darren Vong
"""
from json import loads

from bson import SON
from pymongo import UpdateOne
from pymongo.errors import OperationFailure

from views.helpers import get_current_gameweek, connect

def enforce_injective_name_mapping(col):
    pipeline = [{"$group": {"_id": "$normalised_name", "total": {"$sum": 1}}},
                {"$match": {"total": {"$gt": 1}}}, {"$sort": SON([("total", -1)])}]
    inj_names_pointer = col.aggregate(pipeline)
    new_norm_names = []
    for non_inj_name_obj in inj_names_pointer:
        query = {"normalised_name": non_inj_name_obj["_id"]}
        projection = {"_id": 0, "normalised_name": 1, "first_name": 1}
        # For each repeated name, find all repetitions and their first names
        for rep_name in col.find(query, projection):
            new_norm_names.append({"first_name": rep_name["first_name"],
                                   "normalised_name": rep_name["normalised_name"],
                                   "new_normalised_name": (rep_name["first_name"]+
                                                           u" "+rep_name["normalised_name"].lower())
                                  })
    
    # Update the database with the new normalised names (aka first name + normalised surname)
    updates = [UpdateOne({"normalised_name": p["normalised_name"],
                          "first_name": p["first_name"]},
                         {"$set": {"normalised_name": p["new_normalised_name"]}})
               for p in new_norm_names]
    result = col.bulk_write(updates)
    print result.inserted_count, result.modified_count

def insert_players(col, players):
    """Insert the players data into the database.
    @param col: the MongoDB database collection to insert the player into.
    @param players: this may either be provided as a Python list of players, or a string path
    which points to the JSON file containing the players' data. If a string path is used,
    the keyword argument file_input must be set to True. 
    """
    
    if isinstance(players, (str, unicode)): # Read from file if file path string is given
        with open(players, "rb") as data:
            players_list = [loads(p) for p in data]
    elif isinstance(players, list):
        players_list = players
    else:
        raise RuntimeError("Unknown type passed to param players - "+
                           "should be a list or string path instead")
    
    if col.count() > 0: 
        current_gw = get_current_gameweek(col)
        existing_names = col.database.collection_names(include_system_collections=False)
        validNameFound = False
        while not validNameFound:
            if "gw%d" % current_gw in existing_names:
                current_gw += 0.1
                try:
                    col.rename("gw%0.1f" % current_gw)
                    validNameFound = True
                # Namespace clashes for when I'm too keen and updated db more than once
                except OperationFailure:
                    continue
            else:
                col.rename("gw%d" % current_gw)
                validNameFound = True
    
    col.insert_many(players_list)

def update_heroku_db(local_client, num_cols=2):
    """Utility function as an alternative way of updating the MongoLab version of MongoDB.
    @param local_client: The client connection to a local MongoDB instance.  
    @keyword num_cols: The number of collections of data to transfer from the local
    MongoDB database to the MongoLab database. Default is 2 (current gw + prev available gw).
    """
    
    client, col = connect(on_heroku=True)
    avail_cols = local_client.players.collection_names(include_system_collections=False)
    avail_cols.sort()
    # Puts the "current_gw" collection to the end of the list
    latest = avail_cols.pop(0)
    avail_cols.append(latest)
    
    num_cols *= -1 # So that slice of avail_cols list is taken from the end
    for col in avail_cols[num_cols:]:
        players = [p for p in local_client.players[col].find()]
        result = client.get_default_database()[col].insert_many(players)
        print len(result.inserted_ids)
