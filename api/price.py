# -*- coding: utf-8 -*-

"""
@author: Darren
"""
import numpy as np

import helpers
import attribute

attr = "price"

def get_over_time_data(col, player_name, start, end):
    s, e, query = helpers.init(player_name, start, end)
    projection = {"_id": 0, "gameweeks": {"$slice": ["$fixture_history.gameweek", s, e]},
                  attr: {"$slice": ["$fixture_history."+attribute.INTERNAL_ATTR_MAP[attr], s, e]},
                  "results": {"$slice": ["$fixture_history.opponent_result", s, e]}}
    pipeline = [{"$match": query}, {"$project": projection}]
    data = col.aggregate(pipeline).next()
    data = helpers.pairs_to_lists(zip(data["gameweeks"], data[attr]))
    return map(lambda p: [p[0],p[1]/10.0], data)

def get_changes_data(col, player_name, start, end):
    gw_attr_pairs = get_over_time_data(col, player_name, start, end)
    gameweeks = [gw for gw, _ in gw_attr_pairs]
    attr_vals = np.array([p for _, p in gw_attr_pairs])
    diffs = np.diff(attr_vals)
    diffs = np.around(np.insert(diffs, 0, 0), decimals=1)
    data = map(list, zip(gameweeks, diffs))
    return data