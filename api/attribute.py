# -*- coding: utf-8 -*-

"""
A module containing generic data gatherer (from a MongoDB database) functions
for an 'extensible' attribute on the profile page. 'Extensible' here means the
attribute has more information that can be projected onto the graph on the profile page.
@author: Darren
"""
import numpy as np

import helpers

INTERNAL_ATTR_MAP = {
    "points": "points",
    "goals": "goals",
    "price": "price",
    "assists": "assists",
    "netTransfers": "net_transfers",
    "cleanSheets": "clean_sheet",
    "minutesPlayed": "mins_played"
}

def get_over_time_data(col, player_name, start, end, attr):
    s, e, query = helpers.init(player_name, start, end)
    projection = {"_id": 0, "gameweeks": {"$slice": ["$fixture_history.gameweek", s, e]},
                  attr: {"$slice": ["$fixture_history."+INTERNAL_ATTR_MAP[attr], s, e]},
                  "results": {"$slice": ["$fixture_history.opponent_result", s, e]}}
    pipeline = [{"$match": query}, {"$project": projection}]
    data = col.aggregate(pipeline).next()
    res_length = len(data["gameweeks"])
    data = [{"x": data["gameweeks"][i], "y": data[attr][i], "name": data["results"][i]}
            for i in xrange(res_length)]
#     data = helpers.pairs_to_lists(zip(data["gameweeks"], data[attr]))
    return data

def get_home_vs_away_data(col, player_name, start, end, attr):
    s, e, query = helpers.init(player_name, start, end)
    projection = {"_id": 0, "fixture_history": {"$slice": ["$fixture_history", s, e]}}
    pipeline = [{"$match": query}, {"$project": projection}, {"$unwind": "$fixture_history"},
                {"$group": {"_id": "$fixture_history.ground",
                            "y": {"$sum": "$fixture_history."+INTERNAL_ATTR_MAP[attr]}}}]
    data = [d for d in col.aggregate(pipeline)]
    for d in data:
        d["_id"] = "Home" if d["_id"] == "H" else "Away"
        d["name"] = d.pop("_id")
    return data

def get_consistency_data(col, player_name, start, end, attr):
    s, e, query = helpers.init(player_name, start, end)
    projection = {"_id": 0, attr: {"$slice": ["$fixture_history."+INTERNAL_ATTR_MAP[attr], s, e]}}
    pipeline = [{"$match": query}, {"$project": projection}]
    attr_vals = np.array(col.aggregate(pipeline).next()[attr])
    data = [attr_vals.min(), np.percentile(attr_vals, 25, interpolation="midpoint"), np.median(attr_vals),
            np.percentile(attr_vals, 75, interpolation="midpoint"), attr_vals.max()]
    return [data]

def get_cumulative_total_data(col, player_name, start, end, attr):
    gw_attr_pairs = get_over_time_data(col, player_name, start, end, attr)
    gameweeks = [gw for gw, _ in gw_attr_pairs]
    attr_vals = [p for _, p in gw_attr_pairs]
    cum_sums = np.cumsum(attr_vals)
    data = map(list, zip(gameweeks, cum_sums))
    return data

if __name__ == "__main__":
    from pymongo import MongoClient
    c = MongoClient()
    col = c.players.current_gw
    print get_over_time_data(col, "Vardy", 24, 31, "points")