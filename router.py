# -*- coding: utf-8 -*-

"""
This module is responsible for directing HTTP requests to the
appropriate callback handler functions which in turn return the
appropriate contents (HTML pages).
@author: Darren Vong
"""
import json

from bottle import route, post, static_file, template, redirect, request, response, run

from views import home, helpers, head_to_head, profiles, player_filter

client, players_col = helpers.connect()

@route("/")
def root():
    hot_players = home.get_hot_players(players_col)
    pound_stretchers = home.pound_stretchers(players_col)
    popular_players = home.most_popular(players_col)
    return template("index", hot_players=hot_players, pound_stretchers=pound_stretchers,
                    popular_players=popular_players)

@post("/player_names")
def get_player_names():
    player_names = profiles.get_player_names(players_col)
    response.content_type = "application/json"
    return json.dumps(player_names)

@route("/profile")
def profile():
    return template("profile_home", noResultsFound=False)

@post("/profile")
def get_player_profile():
    player_name = helpers.accent_fold(request.forms.player_name).strip().capitalize()
    try:
        contents = profiles.get_profile_contents(player_name, players_col)
    except StopIteration: # Should never be reached when js is enabled in browser
        return template("profile_home", noResultsFound=True)
    return template("profile", contents=contents)

@post("/graph_data")
def get_graph_data():
    attr, metric, start, end, player_name = (request.forms.attr, request.forms.metric,
                                request.forms.start, request.forms.end,
                                request.forms.player_name)
    return profiles.get_graph_data(metric, int(start), int(end), players_col, player_name, attr)

@route("/head_to_head")
def head_to_head_home():
    return template("h2h_home", noResultsFound=False)

@post("/head_to_head")
def get_head_to_head_page():
    player1 = helpers.accent_fold(request.forms.player1).strip().capitalize()
    player2 = helpers.accent_fold(request.forms.player2).strip().capitalize()
    try:
        player1_profile, player2_profile = head_to_head.get_players_profiles(
                                                            player1, player2, players_col)
    except StopIteration:
        return template("h2h_home", noResultsFound=True)
    return template("head_to_head", p1_profile=player1_profile, p2_profile=player2_profile)

@route("/player_filter")
def multi_player_home():
    return template("player_filter_home",current_gw=helpers.get_current_gameweek(players_col))

@post("/player_filter")
def multi_player_comp():
    player_stats, selected_filters = player_filter.get_table_contents(players_col, request.forms)
    return template("player_filter", player_stats=player_stats,
                    current_gw=helpers.get_current_gameweek(players_col),
                    selected_filters=selected_filters, start=request.forms.start,
                    end=request.forms.end, position=request.forms.position)

@route("<path:path>")
def get_resources(path):
    return static_file(path, root="./")

if __name__ == "__main__":
    run(host='localhost', port=80, reloader=True, debug=True)