# -*- coding: utf-8 -*-

"""
@author: Darren Vong
"""

from bson import SON

# Map the names obtained from the multi-player's page form to the keys
# found in player's data stored in MongoDB
VALUE_TO_DATA_KEY = {
    "points": "points",
    "selectedBy": "selected_by",
    "form": "form",
    "price": "now_cost",
    "goals": "goals",
    "assists": "assists",
    "netTransfers": "net_transfers",
    "minutesPlayed": "mins_played",
    "cleanSheets": "clean_sheet"
}

def get_table_contents(col, form_dict):
    query = None
    projection = {"_id": 0, "fixture_history": 1, "web_name": 1,
                  "normalised_name": 1, "team_name": 1}
    internal_map_keys = VALUE_TO_DATA_KEY.keys()
    for k, v in form_dict.iteritems():
        if k == "position":
            if v != "All":
                query = {"type_name": v} # Not the generic "All", so use it as a query filter
                regroup = {"_id": "$normalised_name", "web_name": {"$first": "$web_name"},
                           "team_name": {"$first": "$team_name"}}
            else:
                # Too generic, so project the player's position to see where in the pitch they play
                projection["type_name"] = 1
                regroup = {"_id": "$normalised_name", "position": {"$first": "$type_name"},
                           "web_name": {"$first": "$web_name"}, "team_name": {"$first": "$team_name"}}
        elif k == "netTransfers":
            projection[VALUE_TO_DATA_KEY[k]] = {"$subtract":
                                                ["$transfers_in_event", "$transfers_out_event"]}
        elif k in internal_map_keys:
            projection[VALUE_TO_DATA_KEY[k]] = 1
    
    selected_filters = get_selected_filters(form_dict)
    # attributes that are affected by game week range filter
    gw_affectables = ["points", "goals", "assists", "minutesPlayed", "cleanSheets"]
    
    # 'attr' refers to the name of the attribute filters available to the user on the GUI
    for attr in VALUE_TO_DATA_KEY.iterkeys():
        if attr in selected_filters:
            if attr in gw_affectables:
                regroup[VALUE_TO_DATA_KEY[attr]] = {"$sum": "$fixture_history."+VALUE_TO_DATA_KEY[attr]}
            else:
                regroup[VALUE_TO_DATA_KEY[attr]] = {"$first": "$"+VALUE_TO_DATA_KEY[attr]}
    
    sorting_order = [("points", -1), ("form", -1), ("selected_by", -1), ("goals", -1),
                     ("assists", -1), ("now_cost", 1), ("net_transfers", -1), ("mins_played", -1)]
    if form_dict.position == "Defender" or form_dict.position == "Goalkeeper":
        sorting_order.insert(4, ("clean_sheet", -1)) # More important than assists for GK or Defender
    else:
        sorting_order.insert(5, ("clean_sheet", -1)) # Just after assists
    
    pipeline = [{"$project": projection}, {"$unwind": "$fixture_history"},
                {"$match": {"fixture_history.gameweek":
                            {"$gte": int(form_dict.start), "$lte": int(form_dict.end)+0.5}}},
                {"$group": regroup},
                {"$sort": SON(sorting_order)},
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
