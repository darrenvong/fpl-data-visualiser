# -*- coding: utf-8 -*-
# @author: Darren Vong

import numpy as np

import helpers

def get_over_time_data(col, player_name, start, end, attr="points"):
    s = start - 1 # "Start" in terms of index
    # "End" in terms of index (technically this is the number of elements to keep
    e = end - start + 1
    if attr == "points":
        query = {"normalised_name": player_name}
        projection = {"_id": 0, "gameweeks": {"$slice": ["$fixture_history.gameweek", s, e]},
                      "points": {"$slice": ["$fixture_history.points", s, e]}}
        pipeline = [{"$match": query}, {"$project": projection}]
        data = col.aggregate(pipeline).next()
        data = map(list, zip(data["gameweeks"], data["points"]))
    return data

if __name__ == "__main__":
    c, col = helpers.connect()
    print get_over_time_data(col, "Ashley williams", 5, 10)