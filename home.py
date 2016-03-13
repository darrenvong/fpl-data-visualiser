# -*- coding: utf-8 -*-

"""
@author: Darren Vong
"""

import helpers
from pymongo import DESCENDING
from bson import SON

def get_hot_players(col):
    query = {"total_points": {"$gt": 0}}
    projection = {"_id": 0, "web_name": 1, "team_name": 1, "now_cost": 1, "total_points": 1,
                  "form": 1}
    cursor = col.find(query, projection, sort=[("form", DESCENDING)], limit=5)
    return [player for player in cursor]

def pound_stretchers(col):
    avg_points = round(find_key_averages(col))
    avg_cost = 50
    query = {"now_cost": {"$lte": avg_cost}, "total_points": {"$gte": avg_points}}
    projection = {"_id": 0, "web_name": 1, "team_name": 1, "now_cost": 1, "total_points": 1}
    cursor = col.find(query, projection, sort=[("total_points", DESCENDING)], limit=5)
    return [player for player in cursor]
        
def find_key_averages(col):
    """Finds the average points and values of all active players in Fantasy Premier League"""
    query = {"total_points": {"$gt": 0}}
    projection = {"_id": 0, "avg_points": 1}
    pipeline = [{"$match": query}, {"$group": {"_id": None, "avg_points": {"$avg": "$total_points"}}},
                {"$project": projection}]
    cursor = col.aggregate(pipeline)
    return cursor.next()["avg_points"]

def most_popular(col):
    projection = {"_id": 0, "web_name": 1, "team_name": 1, "now_cost": 1, "total_points": 1,
                  "net_transfers": {"$subtract": ["$transfers_in_event", "$transfers_out_event"]}}
    pipeline = [{"$project": projection}, {"$sort": SON([("net_transfers", -1)])},
                {"$limit": 5}]
    cursor = col.aggregate(pipeline)
    return [player for player in cursor]

def generate_tables(players_list, table_type="pound_stretchers"):
    table_html = u""
    
    for player in players_list:
        table_html += u"<tr>\n"
        table_html += u"<td>"+player["web_name"]+u"</td>\n"
        table_html += u"<td>"+player["team_name"]+u"</td>\n"
        table_html += u"<td>£"+unicode(player["now_cost"]/10.0)+u"M</td>\n"
        table_html += u"<td>"+unicode(player["total_points"])+u"</td>\n"
        
        if table_type == "hot_players":
            table_html += u"<td>"+player["form"]+u"</td>\n"
        elif table_type == "popular_players":
            transfer_sign = u"+" if player["net_transfers"]>0 else u"-"
            table_html += u"<td>"+transfer_sign+unicode(player["net_transfers"])+u"</td>\n"
        table_html += u"</tr>\n"
    return table_html

if __name__ == "__main__":
    _, players = helpers.connect()
    hot, ps, mp = get_hot_players(players), pound_stretchers(players), most_popular(players)
    hot_table = generate_tables(hot, "hot_players")
    ps_table = generate_tables(ps)
    mp_table = generate_tables(mp, "popular_players")
    print hot_table
    print
    print ps_table
    print
    print mp_table
    