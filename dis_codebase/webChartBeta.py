from bottle import route, run, template, static_file, debug, post, request
from scrapper import getPoints, connect

client = players = None
playData = {}


@route('/graphs')
def show_graph():
    global client, players, playData
    if client is None or players is None:
        client, players = connect()
    if len(playData) == 0:
        for points, weeks, name in getPoints(client, players):
            nameVal = name if name.count(" ")==0 else name.replace(" ", "_")
            playData[nameVal] = map(list, zip(weeks, points))
    return template("hcExamples", playData=playData)

@post('/graphs')
def get_player_data():
    return playData

@post('/secret')
def secret():
    player_obj = {"Vardy": [5,8,5,9], "Lukaku": [1,1,2,5], "Oz": [1,5,15,8]}
    return player_obj

@route('/<name>')
def index(name):
    return template("bottleTemp", name=name)

@route('/favicon.ico')
def get_icon():
    return static_file("favicon.ico", root="../")

@route('/<path:path>')
def get_js(path):
    return static_file(path, root="./")

debug(True)
run(host='localhost', port=8080, reloader=True)