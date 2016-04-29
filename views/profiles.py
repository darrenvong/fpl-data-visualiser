# -*- coding: utf-8 -*-

"""
This module is responsible for any dynamic contents required for the player profiles page
of the system.
@author: Darren Vong
"""
from string import capwords

import profile_graph_api

def get_profile_contents(player_name, col):
    """Finds a player's profile from the system's MongoDB database.
    @param player_name: the normalised (i.e. no accents in characters) name of the player's profile to look for
    @param col: the MongoDB database collection to search the profiles from
    @return a dictionary containing the player's profile data
    """
    
    query = {"normalised_name": player_name}
    projection = {"_id": 0, "web_name": 1,"total_points": 1, "now_cost": 1, "goals_scored": 1,
                  "assists": 1, "clean_sheets": 1, "normalised_name": 1, "status": 1,
                  "net_transfers": {"$subtract": ["$transfers_in_event", "$transfers_out_event"]},
                  "minutes": 1, "yellow_cards": 1, "chance_of_playing_next_round": 1,
                  "fixture_history": 1, "type_name": 1, "photo": 1, "selected_by_percent": 1}
    pipeline = [{"$match": query}, {"$project": projection}]
    cursor = col.aggregate(pipeline)
    profile_contents = cursor.next()
    profile_contents["start_gw"] = int(profile_contents["fixture_history"][0]["gameweek"])
    profile_contents["current_gw"] = int(profile_contents["fixture_history"][-1]["gameweek"])
    return profile_contents

def get_player_names(col):
    """Finds all of the players' names that are in FPL. This is an internal API function used to
    return all player names in a list used to populate the autocomplete widget in the player search bar.
    @param col: the database collection to find the names from
    @return a list consisting of all players currently in FPL
    """
    
    cursor = col.find({}, {"_id": 0, "normalised_name": 1})
    player_names = [custom_capitalise(player_obj["normalised_name"]) for player_obj in cursor]
    return player_names

def custom_capitalise(s):
    """Capitalises every space separated words in s, as opposed to only the first word in the string
    in the default Python implementation. This is purely for aesthetic purpose only for
    when the names are suggested to the user in the autocomplete widget.
    @param s: the string to capitalise
    @return a capitalised copy of s
    """
    
    return capwords(s, " ")

def get_graph_data(metric, start, end, col, player_name, attr):
    """Fetches the data required to plot the graph on the player profiles page.
    @param attr: the attribute data to get
    @param metric: the specific performance metric data of an attribute to get
    @param start: the start game week range of the data
    @param end: the end game week range of the data
    @param col: the database collection to find the player's data from
    @param player_name: the name of the player's data to look for
    @return a dictionary containing the data in the format required to plot the graph
    """
    
    if metric == "over_time":
        return dict(over_time=profile_graph_api.get_over_time_data(
                                                    col, player_name, start, end, attr))
    elif metric == "home_vs_away":
        return dict(home_vs_away=profile_graph_api.get_home_vs_away_data(
                                                    col, player_name, start, end, attr))
    elif metric == "consistency":
        return dict(consistency=profile_graph_api.get_consistency_data(
                                                    col, player_name, start, end, attr))
    elif metric == "cum_total":
        return dict(cum_total=profile_graph_api.get_cumulative_total_data(
                                                    col, player_name, start, end, attr))
    elif metric == "events_breakdown":
        return dict(events_breakdown=profile_graph_api.get_events_breakdown_data(
                                                    col, player_name, start, end, attr))
    elif metric == "changes": # Currently only applicable to prices
        return dict(changes=profile_graph_api.get_changes_data(
                                                    col, player_name, start, end, attr))
