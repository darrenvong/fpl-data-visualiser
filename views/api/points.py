# -*- coding: utf-8 -*-

"""
@author: Darren
"""
import numpy as np

import helpers
from helpers import pairs_to_lists
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
    if player_type == 4: # Forwards
        return map(lambda x: 4*x, goals)
    elif player_type == 3: # Midfields
        return map(lambda x: 5*x, goals)
    else: # Defenders/GKs
        return map(lambda x: 6*x, goals)

def get_events_breakdown_data(col, player_name, start, end):
    pipeline = helpers.init(player_name, start, end)
    pipeline[1]["$project"]["element_type"] = 1
    projection = [{"$group": {"_id": None, "goals": {"$push": "$fixture_history.goals"},
                  "assists": {"$push": "$fixture_history.assists"},
                  "clean_sheets": {"$push": "$fixture_history.clean_sheet"},
                  "points": {"$push": "$fixture_history.points"},
                  "gameweeks": {"$push": "$fixture_history.gameweek"},
                  "player_type": {"$first": "$element_type"}}}]
    pipeline.extend(projection)
    breakdown_object = col.aggregate(pipeline).next()
    
    goal_points = get_goal_points(breakdown_object["goals"], breakdown_object["player_type"])
    assist_points = map(lambda x: 3*x, breakdown_object["assists"])
    others_points = (np.array(breakdown_object["points"]) - np.array(goal_points)
                     - np.array(assist_points))
    data = [{"goals": pairs_to_lists(zip(breakdown_object["gameweeks"],goal_points))},
            {"assists": pairs_to_lists(zip(breakdown_object["gameweeks"],assist_points))}]
    if breakdown_object["player_type"] == 3 or breakdown_object["player_type"] == 4: # Forwards/midfields
        data.append({"others": pairs_to_lists(zip(breakdown_object["gameweeks"],others_points.tolist()))})
    else: # Defenders/GKs
        cs_points = map(lambda x: 4*x, breakdown_object["clean_sheets"])
        others_points -= np.array(cs_points)
        data.extend([{"cleanSheets": pairs_to_lists(zip(breakdown_object["gameweeks"],cs_points))},
                     {"others": pairs_to_lists(zip(breakdown_object["gameweeks"],others_points.tolist()))}])
    return data