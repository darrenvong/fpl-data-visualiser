from bottle import *
from scrapper import getPoints, connect

class WebChartProg(Bottle):

    def __init__(self, *args, **kwargs):
        super(WebChartProg, self).__init__(*args, **kwargs)
        self.client = self.players = None
        self.playerData = {}
        self._route()
    
    def _route(self):
        self.route('/graphs', callback=self.show_graph)
        self.post('/graphs', callback=self.get_player_data)
        self.route('/<n>', callback=lambda n: self.index(n))
        self.route('/favicon.ico', callback=self.get_icon)
        self.route('/<path:path>', callback=lambda path: self.get_js(path))
    
    def show_graph(self):
        if self.client is None or self.players is None:
            self.client, self.players = connect()
        if len(self.playerData) == 0:
            for points, weeks, name in getPoints(self.client, self.players):
                nameVal = name if name.count(" ")==0 else name.replace(" ", "_")
                self.playerData[nameVal] = map(list, zip(weeks, points))
        return template("hcExamples", playData=self.playerData)
    
    def get_player_data(self):
        return self.playerData
    
    def index(self, n):
        return "<!DOCTYPE html><html><head></head><body>Hello "+n+"</body></html>"
    
    def get_icon(self):
        return static_file("favicon.ico", root="../")
    
    def get_js(self, path):
        return static_file(path, root="./")

if __name__ == '__main__':
    app = WebChartProg()
    app.run(host='localhost', port=80, reloader=True, debug=True)