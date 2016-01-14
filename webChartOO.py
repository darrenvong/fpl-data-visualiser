from bottle import *
from scrapper import getPoints, connect

class WebChartProg(Bottle):

    def __init__(self, *args, **kwargs):
        Bottle.__init__(self, *args, **kwargs)
        self.client, self.players = connect()
        self.playerData = {}
        self._route()
    
    def _route(self):
        self.route('/graphs', callback=self.show_graph)
        self.route('/graphs', method="POST", callback=self.get_player_data)
        self.route('/secret', method="POST", callback=self.secret)
        self.route('/<n>', callback=lambda n: self.index(n))
        self.route('/favicon.ico', callback=self.get_icon)
        self.route('/<path:path>', callback=lambda path: self.get_js(path))
    
    def show_graph(self):
        for points, weeks, name in getPoints(self.client, self.players):
            nameVal = name if name.count(" ")==0 else name.replace(" ", "_")
            self.playerData[nameVal] = map(list, zip(weeks, points))
        return template("hcExamples", playData=self.playerData)
    
    def get_player_data(self):
        return self.playerData
    
    def secret(self):
        player_obj = {"Vardy": [5,8,5,9], "Lukaku": [1,1,2,5], "Oz": [1,5,15,8]}
        return player_obj
    
    def index(self, n):
        return template("bottleTemp", name=n)
    
    def get_icon(self):
        return static_file("favicon.ico", root="../")
    
    def get_js(self, path):
        return static_file(path, root="./")

if __name__ == '__main__':
    app = WebChartProg()
    app.run(host='localhost', port=8080, reloader=True, debug=True)