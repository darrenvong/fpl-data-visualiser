"""
Created on 21 Feb 2016
@author: Darren Vong
"""
from bottle import Bottle, static_file, template, redirect
import home

class Router(Bottle):
    """This class is responsible for directing requests to callback handler functions
    and subsequently return the appropriate contents."""

    def __init__(self, *args, **kwargs):
        """Starts the visualiser application."""
        
        super(Router, self).__init__(*args, **kwargs)
        self.client = self.players_col = None
        self._route()
    
    def _route(self):
        """A pseudo-private method for binding callback functions to the different
        end points (i.e. URL paths) of the application."""
        
        self.route("/", callback=self.re_route)
        self.route("/index", callback=self.root)
        self.route("/profiles", callback=self.profiles)
        self.route("<path:path>", callback=lambda path: self.get_resources(path))
    
    def _establish_db_connection(self):
        if self.client is None:
            self.client, self.players_col = home.connect()
    
    def root(self):
        self._establish_db_connection()
        hot_players = home.get_hot_players(self.players_col)
        pound_stretchers = home.pound_stretchers(self.players_col)
        popular_players = home.most_popular(self.players_col)
        return template("index", hot_players=hot_players, pound_stretchers=pound_stretchers,
                        popular_players=popular_players)
    
    def re_route(self):
        """Redirects the 'true' root to the /index end point where a root page is
        actually defined."""
        redirect("/index")

    def profiles(self):
        return template("profiles")
    
    def get_resources(self, path):
        return static_file(path, root="./")

if __name__ == "__main__":
    visualiser = Router()
    visualiser.run(host='localhost', port=80, reloader=True, debug=True)