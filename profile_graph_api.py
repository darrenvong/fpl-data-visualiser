# -*- coding: utf-8 -*-
# @author: Darren Vong

import numpy as np

import helpers

def to_indices(start, end):
    """Helper function for converting game week numbers in terms of index nums
    which corresponds to the location of where things should be stored internally"""
    return start-1, end-start+1

def get_over_time_data(col, player_name, start, end, attr):
    s, e = to_indices(start, end)
    query = {"normalised_name": player_name}
    if attr == "points":
        projection = {"_id": 0, "gameweeks": {"$slice": ["$fixture_history.gameweek", s, e]},
                      "points": {"$slice": ["$fixture_history.points", s, e]}}
        pipeline = [{"$match": query}, {"$project": projection}]
        data = col.aggregate(pipeline).next()
        data = map(list, zip(data["gameweeks"], data["points"]))
    return data

def get_home_vs_away_data(col, player_name, start, end, attr):
    s, e = to_indices(start, end)
    query = {"normalised_name": player_name}
    if attr == "points":
        projection = {"_id": 0, "fixture_history": {"$slice": ["$fixture_history", s, e]}}
        pipeline = [{"$match": query}, {"$project": projection}, {"$unwind": "$fixture_history"},
                    {"$group": {"_id": "$fixture_history.ground",
                                "y": {"$sum": "$fixture_history.points"}}}]
        data = [d for d in col.aggregate(pipeline)]
        for d in data:
            d["_id"] = "Home" if d["_id"] == "H" else "Away"
            d["name"] = d.pop("_id")
    return data

def get_consistency_data(col, player_name, start, end, attr):
    s, e = to_indices(start, end)
    query = {"normalised_name": player_name}
    if attr == "points":
        projection = {"_id": 0, "points": {"$slice": ["$fixture_history.points", s, e]}}
        pipeline = [{"$match": query}, {"$project": projection}]
        points = np.array(col.aggregate(pipeline).next()["points"])
        data = [points.min(), np.percentile(points, 25, interpolation="midpoint"), np.median(points),
                np.percentile(points, 75, interpolation="midpoint"), points.max()]
    return [data]

def get_cumulative_total_data(col, player_name, start, end, attr="points"):
    if attr == "points":
        gw_points_list = get_over_time_data(col, player_name, start, end, attr)
        gameweeks = [gw for gw, _ in gw_points_list]
        points = [p for _, p in gw_points_list]
        cum_sums = np.cumsum(points)
        data = map(list, zip(gameweeks, cum_sums))
    return data

def get_goal_points(goals, player_type):
    if player_type == 4: # Forward
        return map(lambda x: 4*x, goals)
    elif player_type == 3: # Midfield
        return map(lambda x: 5*x, goals)
    else: # Defender or GK
        return map(lambda x: 6*x, goals)

def get_events_breakdown_data(col, player_name, start, end, attr):
    s, e = to_indices(start, end)
    query = {"normalised_name": player_name}
    if attr == "points":
        projection = {"_id": 0, "goals": {"$slice": ["$fixture_history.goals_scored", s, e]},
                      "assists": {"$slice": ["$fixture_history.assists", s, e]},
                      "points": {"$slice": ["$fixture_history.points", s, e]},
                      "player_type": "$element_type"}
        pipeline = [{"$match": query}, {"$project": projection}]
        breakdown_object = col.aggregate(pipeline).next()
        goal_points = get_goal_points(breakdown_object["goals"], breakdown_object["player_type"])
        assist_points = map(lambda x: 3*x, breakdown_object["assists"])
        others_points = (np.array(breakdown_object["points"]) - np.array(goal_points) -
                         np.array(assist_points))
        data = [{"name": "Goals", "data": goal_points}, {"name": "Assists", "data": assist_points},
                {"name": "Others", "data": others_points.tolist()}]
    return data

if __name__ == "__main__":
    c, col = helpers.connect()
    print get_over_time_data(col, "Vardy", 5, 14, "points")
    print get_home_vs_away_data(col, "Vardy", 5, 14, "points")
    print get_consistency_data(col, "Vardy", 5, 14, "points")
    print get_cumulative_total_data(col, "Vardy", 5, 14, "points")
    print get_events_breakdown_data(col, "Vardy", 5, 14, "points")
    c.close()