# -*- coding: utf-8 -*-

"""
@author: Darren Vong
"""

from bson import SON

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

def get_table_contents(col, form_dict):
    query = None
    projection = {"_id": 0, "fixture_history": 1, "web_name": 1}
    internal_map_keys = VALUE_TO_DATA_KEY.keys()
    for k, v in form_dict.iteritems():
        if k == "position" and v != "all":
            query = {"type_name": v}
        elif k == "netTransfers":
            projection[VALUE_TO_DATA_KEY[k]] = {"$subtract":
                                                ["$transfers_in_event", "$transfers_out_event"]}
        elif k in internal_map_keys:
            projection[VALUE_TO_DATA_KEY[k]] = 1
    print projection
    regroup = {"_id": "$web_name", "total_points": {"$sum": "$fixture_history.points"},
               "selected_by": {"$first": "$selected_by"}, "form": {"$first": "$form"},
               "now_cost": {"$first": "$now_cost"}, "goals_scored": {"$first": "$goals_scored"},
               "assists": {"$first": "$assists"},"net_transfers": {"$first": "$net_transfers"},
               "minutes": {"$first": "$minutes"},
               "points_detailed": {"$push": {"gameweek": "$fixture_history.gameweek",
                                             "pts": "$fixture_history.points"}}}
    pipeline = [{"$project": projection}, {"$unwind": "$fixture_history"},
                {"$match": {"fixture_history.gameweek":
                            {"$gte": int(form_dict.start), "$lte": int(form_dict.end)+0.5}}},
                {"$group": regroup},
                {"$sort": SON([("total_points", -1), ("selected_by", -1), ("form", -1),
                            ("now_cost", 1), ("goals_scored", -1), ("assists", -1),
                            ("net_transfers", -1), ("minutes", -1)])},
                {"$limit": int(form_dict.num_players)}]
    if query is not None:
        pipeline.insert(0, {"$match": query})
    cursor = col.aggregate(pipeline)
    return [player for player in cursor]