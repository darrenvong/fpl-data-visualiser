# -*- coding: utf-8 -*-

"""
@author: Darren
"""
def to_indices(start, end):
    """Helper function for converting game week numbers in terms of index nums
    which corresponds to the location of where things should be stored internally"""
    return start-1, end-start+1

def create_filter_doc(player_name):
    return {"normalised_name": player_name}

def init(player_name, start, end):
    """The standard boilerplate code before each MongoDB query"""
    s, e = to_indices(start, end)
    query_filter = create_filter_doc(player_name)
    return s, e, query_filter

def pairs_to_lists(pairs_list):
    """Converts a list of pairs to a list of (list) pairs
    E.g. [(1,2),(2,3),(3,4)] -> [[1,2], [2,3], [3,4]]"""
    return map(list, pairs_list)