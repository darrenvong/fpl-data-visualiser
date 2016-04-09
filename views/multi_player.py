# -*- coding: utf-8 -*-

"""
@author: Darren Vong
"""

from bson import SON

import helpers

# Map the names obtained from the multi-player's page form to the keys
# found in player's data stored in MongoDB
VALUE_TO_DATA_KEY = {
    "points": "total_points",
    "selectedBy": "selected_by",
    "form": "form",
    "price": "now_cost",
    "goals": "goals_scored",
    "assists": "assists",
    "netTransfers": "net_transfers",
    "minutesPlayed": "minutes"
}

DATA_KEY_TO_DISPLAYED_ATTR = dict([(v, helpers.capitalise_camel_case_words(k))
                                   for k, v in VALUE_TO_DATA_KEY.iteritems()])

def get_table_contents(col, form_dict):
    query = None
    projection = {"_id": 0, "fixture_history": 1, "web_name": 1, "normalised_name": 1}
    internal_map_keys = VALUE_TO_DATA_KEY.keys()
    for k, v in form_dict.iteritems():
        if k == "position":
            if v != "All":
                query = {"type_name": v} # Not the generic "All", so use it as a query filter
                regroup = {"_id": "$normalised_name", "web_name": {"$first": "$web_name"}}
            else:
                # Too generic, so project the player's position to see where in the pitch they play
                projection["type_name"] = 1
                regroup = {"_id": "$normalised_name", "position": {"$first": "$type_name"},
                           "web_name": {"$first": "$web_name"}}
        elif k == "netTransfers":
            projection[VALUE_TO_DATA_KEY[k]] = {"$subtract":
                                                ["$transfers_in_event", "$transfers_out_event"]}
        elif k in internal_map_keys:
            projection[VALUE_TO_DATA_KEY[k]] = 1
    
    selected_filters = get_selected_filters(form_dict)
    # 'value' refers to the name of the attribute filters available to the user on the GUI
    for value in VALUE_TO_DATA_KEY.iterkeys():
        if value in selected_filters:
            if value == "points":
                regroup[VALUE_TO_DATA_KEY[value]] = {"$sum": "$fixture_history.points"}
                regroup["points_detailed"] = {"$push": {"gameweek": "$fixture_history.gameweek",
                                                        "pts": "$fixture_history.points"}}
            else:
                regroup[VALUE_TO_DATA_KEY[value]] = {"$first": "$"+VALUE_TO_DATA_KEY[value]}
    
    pipeline = [{"$project": projection}, {"$unwind": "$fixture_history"},
                {"$match": {"fixture_history.gameweek":
                            {"$gte": int(form_dict.start), "$lte": int(form_dict.end)+0.5}}},
                {"$group": regroup},
                {"$sort": SON([("total_points", -1), ("form", -1), ("selected_by", -1),
                            ("goals_scored", -1), ("assists", -1), ("now_cost", 1),
                            ("net_transfers", -1), ("minutes", -1)])},
                {"$limit": int(form_dict.num_players)}]
    if query is not None:
        pipeline.insert(0, {"$match": query})
    cursor = col.aggregate(pipeline)
    return [player for player in cursor], selected_filters

def get_selected_filters(form_dict):
    return [f for f in form_dict.iterkeys() if f not in ["start", "end", "position", "num_players"]]

def get_previous_position_state(state_val):
    init_pos_options = """<option value='All'>All</option>
                <option value='Goalkeeper'>Goalkeepers</option>
                <option value='Defender'>Defenders</option>
                <option value='Midfielder'>Midfielders</option>
                <option value='Forward'>Forwards</option>"""
    return init_pos_options.replace("'"+state_val+"'", "'"+state_val+"'"+" selected", 1)
