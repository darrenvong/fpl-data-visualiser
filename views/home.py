# -*- coding: utf-8 -*-

"""
This module is responsible for any dynamic contents required for the home page
of the system. 
@author: Darren Vong
"""
from pymongo import DESCENDING
from bson import SON

def get_hot_players(col):
    """Finds the top five most in form players determined by the form scored
    which is calculated as the average points scored in all games played in the last 30 days.
    @param col: the database collection to search the players from
    @return a list containing the top five players accompanied with details such as their price,
    team and total points scored so far this season
    """
    
    query = {"total_points": {"$gt": 0}}
    projection = {"_id": 0, "web_name": 1, "team_name": 1, "now_cost": 1, "total_points": 1,
                  "form": 1}
    cursor = col.find(query, projection, sort=[("form", DESCENDING)], limit=5)
    return [player for player in cursor]

def pound_stretchers(col):
    """Finds the top five bargain players in the game. This is defined to be the players
    who scored above the average points of all active players whilst having a price tag below £5M.
    @param col: the database collection to search the players from
    @return a list containing the top five bargain players accompanied with other details
    such as their team and total points scored so far this season
    """
    
    avg_points = round(find_key_averages(col))
    avg_cost = 50
    query = {"now_cost": {"$lte": avg_cost}, "total_points": {"$gte": avg_points}}
    projection = {"_id": 0, "web_name": 1, "team_name": 1, "now_cost": 1, "total_points": 1}
    cursor = col.find(query, projection, sort=[("total_points", DESCENDING)], limit=5)
    return [player for player in cursor]
        
def find_key_averages(col):
    """Auxiliary function for pound_stretchers function above: finds the average points
    and values of all active players in Fantasy Premier League.
    @param col: the database collection to perform the query on
    @return the value of the average points scored by all active players in FPL
    """
    
    query = {"total_points": {"$gt": 0}}
    projection = {"_id": 0, "avg_points": 1}
    pipeline = [{"$match": query}, {"$group": {"_id": None, "avg_points": {"$avg": "$total_points"}}},
                {"$project": projection}]
    cursor = col.aggregate(pipeline)
    return cursor.next()["avg_points"]

def most_popular(col):
    """Finds the top five players who have the highest net transfer figures in the current game week.
    @param col: the database collection to perform the query on
    @return a list of the top five players who have the highest net transfers, accompanied with other
    details such as their team name, price and total points scored
    """
    
    projection = {"_id": 0, "web_name": 1, "team_name": 1, "now_cost": 1, "total_points": 1,
                  "net_transfers": {"$subtract": ["$transfers_in_event", "$transfers_out_event"]}}
    pipeline = [{"$project": projection}, {"$sort": SON([("net_transfers", -1)])},
                {"$limit": 5}]
    cursor = col.aggregate(pipeline)
    return [player for player in cursor]

def generate_tables(players_list, table_type="pound_stretchers"):
    """Generate tables for the home page using the list of players found from calling
    one of the top players finding functions in this module.
    @param players_list: the list of players to be used to populate the table
    @keyword table_type: the top players category the table is displaying. Defaults to "pound_stretchers"
    since it is the only table which shares common table rows with the other tables on the page
    @return the HTML for the home page template to render the table on page
    """
    
    table_html = u""
    
    for player in players_list:
        table_html += u"<tr>\n"
        table_html += u"<td>"+player["web_name"]+u"</td>\n"
        table_html += u"<td>"+player["team_name"]+u"</td>\n"
        table_html += u"<td>£"+unicode(player["now_cost"]/10.0)+u"M</td>\n"
        table_html += u"<td>"+unicode(player["total_points"])+u"</td>\n"
        
        if table_type == "hot_players":
            table_html += u"<td>"+unicode(player["form"])+u"</td>\n"
        elif table_type == "popular_players":
            transfer_sign = u"+" if player["net_transfers"]>0 else u"-"
            table_html += u"<td>"+transfer_sign+unicode(player["net_transfers"])+u"</td>\n"
        table_html += u"</tr>\n"
    return table_html
