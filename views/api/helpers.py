# -*- coding: utf-8 -*-

"""
@author: Darren
"""
def to_indices(start, end):
    """Helper function for converting game week numbers in terms of index nums
    which corresponds to the location of where things should be stored internally"""
    return start-1, end-start+1


def init(player_name, start, end):
    """The standard boilerplate code before each MongoDB query, which returns only those
    fixture documents which are between the start and end game week values"""
    query = {"normalised_name": player_name}
    projection = {"_id": 0, "fixture_history": 1}
    # +0.5 in "$lte" to account for double game week
    init_pipeline = [{"$match": query}, {"$project": projection}, {"$unwind": "$fixture_history"},
                {"$match": {"fixture_history.gameweek": {"$gte": start, "$lte": end+0.5}}}]
    return init_pipeline

def pairs_to_lists(pairs_list):
    """Converts a list of pairs to a list of (list) pairs
    E.g. [(1,2),(2,3),(3,4)] -> [[1,2], [2,3], [3,4]]"""
    return map(list, pairs_list)