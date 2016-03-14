# -*- coding: utf-8 -*-

"""
@author: Darren Vong
"""

import helpers

def get_profile_contents(player_name, col):
    query = {"web_name": player_name}
    projection = {"_id": 0, "total_points": 1, "now_cost": 1, "goals_scored": 1, "assists": 1,
                  "clean_sheets": 1,
                  "net_transfers": {"$subtract": ["$transfers_in_event", "$transfers_out_event"]},
                  "minutes": 1, "yellow_cards": 1, "chance_of_playing_next_round": 1,
                  "fixture_history": 1, "type_name": 1, "photo": 1, "selected_by_percent": 1}
    pipeline = [{"$match": query}, {"$project": projection}]
    cursor = col.aggregate(pipeline)
    profile_contents = cursor.next()
    profile_contents["current_gw"] = profile_contents["fixture_history"][-1]["gameweek"]
    return profile_contents

if __name__ == '__main__':
    client, players = helpers.connect()
    print get_profile_contents(u"Mahrez", players)
    client.close()