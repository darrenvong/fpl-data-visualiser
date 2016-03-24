# -*- coding: utf-8 -*-

"""
@author: Darren Vong
"""
import json

from bottle import Bottle, static_file, template, redirect, request, response

import home
import helpers
import profiles

class Router(Bottle):
    """This class is responsible for directing HTTP requests to the
    appropriate callback handler functions which in turn return the
    appropriate contents (HTML pages)."""

    def __init__(self, *args, **kwargs):
        """Starts the visualiser application."""
        
        super(Router, self).__init__(*args, **kwargs)
        self.client, self.players_col = helpers.connect()
        self._route()
    
    def _route(self):
        """A pseudo-private method for binding callback functions to the different
        end points (i.e. URL paths) of the application."""
        
        self.route("/", callback=self.re_route)
        self.route("/index", callback=self.root)
        self.route("/profile", callback=self.profiles)
        self.post("/profile", callback=self.get_player_profile)
        self.post("/player_names", callback=self.get_player_names)
        self.route("<path:path>", callback=lambda path: self.get_resources(path))
    
    def root(self):
        hot_players = home.get_hot_players(self.players_col)
        pound_stretchers = home.pound_stretchers(self.players_col)
        popular_players = home.most_popular(self.players_col)
        return template("index", hot_players=hot_players, pound_stretchers=pound_stretchers,
                        popular_players=popular_players)
    
    def re_route(self):
        """Redirects the 'true' root to the /index end point where a root page is
        actually defined."""
        redirect("/index")

    def get_player_names(self):
        player_names = profiles.get_player_names(self.players_col)
        response.content_type = "application/json"
        return json.dumps(player_names)
    
    def profiles(self):
        return template("profile_home")
    
    def get_player_profile(self):
        player_name = helpers.accent_fold(request.forms.getunicode("player_name")).capitalize()
        try:
            contents = profiles.get_profile_contents(player_name, self.players_col)
        except StopIteration: # Should never be reached
            raise RuntimeError("There's an error with the player search function")
        return template("profile", contents=contents)
    
    def get_resources(self, path):
        return static_file(path, root="./")

if __name__ == "__main__":
    visualiser = Router()
    visualiser.run(host='localhost', port=80, reloader=True, debug=True)