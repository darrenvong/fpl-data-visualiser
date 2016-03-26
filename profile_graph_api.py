# -*- coding: utf-8 -*-

"""
@author: Darren Vong
"""
from api import points, price, goals, assists, clean_sheets, net_transfers,\
    mins_played
import helpers

def get_over_time_data(col, player_name, start, end, attr):
    if attr == "points":
        data = points.get_over_time_data(col, player_name, start, end)
    elif attr == "price":
        data = price.get_over_time_data(col, player_name, start, end)
    elif attr == "goals":
        data = goals.get_over_time_data(col, player_name, start, end)
    elif attr == "assists":
        data = assists.get_over_time_data(col, player_name, start, end)
    elif attr == "cleanSheets":
        data = clean_sheets.get_over_time_data(col, player_name, start, end)
    elif attr == "netTransfers":
        data = net_transfers.get_over_time_data(col, player_name, start, end)
    elif attr == "minutesPlayed":
        data = mins_played.get_over_time_data(col, player_name, start, end)
    else: # Should never get hit
        raise RuntimeError("Something went wrong with the API call")
    return data

def get_home_vs_away_data(col, player_name, start, end, attr):
    if attr == "points":
        data = points.get_home_vs_away_data(col, player_name, start, end)
    elif attr == "goals":
        data = goals.get_home_vs_away_data(col, player_name, start, end)
    elif attr == "assists":
        data = assists.get_home_vs_away_data(col, player_name, start, end)
    elif attr == "cleanSheets":
        data = clean_sheets.get_home_vs_away_data(col, player_name, start, end)
    return data

def get_consistency_data(col, player_name, start, end, attr):
    if attr == "points":
        data = points.get_consistency_data(col, player_name, start, end)
    return data

def get_cumulative_total_data(col, player_name, start, end, attr):
    if attr == "points":
        data = points.get_cumulative_total_data(col, player_name, start, end)
    elif attr == "goals":
        data = goals.get_cumulative_total_data(col, player_name, start, end)
    elif attr == "assists":
        data = assists.get_cumulative_total_data(col, player_name, start, end)
    elif attr == "cleanSheets":
        data = clean_sheets.get_cumulative_total_data(col, player_name, start, end)
    return data

def get_events_breakdown_data(col, player_name, start, end, attr):
    if attr == "points":
        data = points.get_events_breakdown_data(col, player_name, start, end)
    return data

def get_changes_data(col, player_name, start, end, attr):
    data = price.get_changes_data(col, player_name, start, end)
    return data

if __name__ == "__main__":
    c, col = helpers.connect()
    print get_events_breakdown_data(col, "Vardy", 5, 14, "points")
    c.close()