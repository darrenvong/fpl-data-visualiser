# -*- coding: utf-8 -*-

"""
@author: Darren Vong
"""
import urllib2
import json
from time import sleep
from collections import OrderedDict

from views.helpers import accent_fold, headers

# idea adapted from Pringle's (2014) code
FIXTURE_KEY_MAP = {
    0 : "date", 
    1 : "gameweek",
    2 : "opponent_result", 
    3 : "mins_played", 
    4 : "goals",
    5 : "assists",
    6 : "clean_sheet",
    7 : "goals_conceded",
    8 : "own_goals",
    9 : "pens_saved",
    10 : "pens_missed",
    11 : "yellow_cards",
    12 : "red_cards",
    13 : "saves",
    14 : "bonus_points",
    15 : "ea_sports_ppi",
    16 : "bonus_point_system",
    17 : "net_transfers",
    18 : "price",
    19 : "points"
}

def restructure_fixture_data(player_data):
    fixture_objects_list = []
    for fixture in player_data["fixture_history"]["all"]:
        fixture_object = OrderedDict()
        for i in xrange(20):
            fixture_object[FIXTURE_KEY_MAP[i]] = fixture[i]
        fixture_object["ground"] = fixture_object["opponent_result"][4]
        # Handles double game week issues
        if len(fixture_objects_list) > 0:
            if fixture_objects_list[-1]["gameweek"] == fixture_object["gameweek"]:
                fixture_object["gameweek"] += 0.1 # So that both matches data can be plotted
        fixture_objects_list.append(fixture_object)
    player_data["fixture_history"] = fixture_objects_list
    return player_data

def update_db(col, fix_hist_list):
    counter = 0
    for fixture_list in fix_hist_list:
        query = {"web_name": fixture_list["name"]}
        update = {"$set": {"fixture_history": fixture_list["fixture_history"]}}
        result = col.update_one(query, update)
        counter += result.modified_count
    print str(counter)+" affected!"
    
def normalise_names(player_data):
    normalised = accent_fold(player_data["web_name"]).capitalize()
    player_data["normalised_name"] = normalised
    return player_data

def restructure_players_schema(player_data):
    player_data = normalise_names( restructure_fixture_data(player_data) )
    attributes_to_cast = ["selected_by", "selected_by_percent", "form", "points_per_game", "ep_next"]
    for attr in attributes_to_cast:
        player_data[attr] = float(player_data[attr])
    return player_data

def scrape_players(outFile=False):
    """Collects players data from the Fantasy Premier League unofficial API.
    If outFile is set to True, the collected data is written to a JSON file instead.
    @return: players - a list of players data collected. This list is empty if outFile
    is set to True.
    """
    
    address = "http://fantasy.premierleague.com/web/api/elements/"
    i = 1
    players = []
    allFetched = False
    if outFile: output_file = open("FPLdata.json", "wb")
    
    while not allFetched:
        try:
            request = urllib2.Request(address+str(i)+"/", None, headers)
            feed = urllib2.urlopen(request)
            player_data = json.load(feed, object_pairs_hook=OrderedDict)
            player_data = restructure_players_schema(player_data)
            if outFile:
                json_string_data = json.dumps(player_data)
                output_file.write(json_string_data+"\n")
            else:
                players.append(player_data)
        except urllib2.HTTPError:
            print "All players fetched"
            allFetched = True
        except urllib2.URLError:
            print "No internet connection available.", \
                "Please try again later when you are connected to the internet!"
            sleep(10)
            continue
        except ValueError:
            print "Invalid JSON, try again!"
            continue
        else:
            i += 1
        
        if i%5 == 0:
            print "%d players scraped" % (i-1)
            if outFile: output_file.flush()
            sleep(3)
       
    if outFile: output_file.close()
    print "Data collection... done!"
    return players
