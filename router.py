"""
Created on 21 Feb 2016
@author: Darren Vong
"""
from bottle import Bottle, static_file, template, redirect

class Router(Bottle):
    """This class is responsible for directing requests to callback handler functions
    and subsequently return the appropriate contents."""

    def __init__(self, *args, **kwargs):
        """Starts the visualiser application."""
        
        super(Router, self).__init__(*args, **kwargs)
        self._route()
    
    def _route(self):
        """A pseudo-private method for binding callback functions to the different
        end points (i.e. URL paths) of the application."""
        
        self.route("/", callback=self.re_route)
        self.route("/index", callback=self.root)
        self.route("<path:path>", callback=lambda path: self.get_resources(path))
    
    def root(self):
        return template("index")
    
    def re_route(self):
        redirect("/index")
    
    def get_resources(self, path):
        return static_file(path, root="./")

if __name__ == "__main__":
    visualiser = Router()
    visualiser.run(host='localhost', port=80, reloader=True, debug=True)