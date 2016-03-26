# -*- coding: utf-8 -*-

"""
@author: Darren
"""
import numpy as np

import helpers
import attribute

attr = "points"

def get_over_time_data(col, player_name, start, end):
    data = attribute.get_over_time_data(col, player_name, start, end, attr)
    return data

def get_home_vs_away_data(col, player_name, start, end):
    data = attribute.get_home_vs_away_data(col, player_name, start, end, attr)
    return data

def get_consistency_data(col, player_name, start, end):
    return attribute.get_consistency_data(col, player_name, start, end, attr)

def get_cumulative_total_data(col, player_name, start, end):
    return attribute.get_cumulative_total_data(col, player_name, start, end, attr)

def get_goal_points(goals, player_type):
    return map(lambda x: 4*x, goals) if player_type == 4 else map(lambda x: 5*x, goals)

def get_events_breakdown_data(col, player_name, start, end):
    s, e, query = helpers.init(player_name, start, end)
    projection = {"_id": 0, "goals": {"$slice": ["$fixture_history.goals", s, e]},
                  "assists": {"$slice": ["$fixture_history.assists", s, e]},
                  "clean_sheets": {"$slice": ["$fixture_history.clean_sheet", s, e]},
                  "points": {"$slice": ["$fixture_history.points", s, e]},
                  "player_type": "$element_type"}
    pipeline = [{"$match": query}, {"$project": projection}]
    breakdown_object = col.aggregate(pipeline).next()
    
    goal_points = get_goal_points(breakdown_object["goals"], breakdown_object["player_type"])
    assist_points = map(lambda x: 3*x, breakdown_object["assists"])
    others_points = (np.array(breakdown_object["points"]) - np.array(goal_points)
                     - np.array(assist_points))
    data = [{"name": "Goals", "data": goal_points}, {"name": "Assists", "data": assist_points}]
    if breakdown_object["player_type"] == 3 or breakdown_object["player_type"] == 4: # Forwards/midfields
        data.append({"name": "Others", "data": others_points.tolist()})
    else: # Defenders/GKs
        cs_points = map(lambda x: 4*x, breakdown_object["clean_sheets"])
        others_points -= np.array(cs_points)
        data.extend([{"name": "Clean sheets", "data": cs_points},
                     {"name": "Others", "data": others_points.tolist()}])
    return data