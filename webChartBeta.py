from bottle import route, run, template, static_file, debug, post, redirect
from scrapper import getPoints

i = 0

@route('/graphs')
def show_graph():
    playData = {}
    for points, weeks, name in getPoints():
        nameVal = name if name.count(" ")==0 else name.replace(" ", "_")
        playData[nameVal] = map(list, zip(weeks, points))
    return template("hcExamples", playData=playData)

@post('/secret')
def secret():
    players_list = ["Kante", "Lukaku", "Vardy"]
    global i
    i = i+1 if i<2 else 0
    return players_list[i]

@route('/<name>')
def index(name):
    return template("bottleTemp", name=name)

@route('/favicon.ico')
def get_icon(path="favicon.ico"):
    return static_file(path, root="../")

@route('/<path:path>')
def get_js(path):
    return static_file(path, root="./")

# @route('js/<path:path>')
# def get_js2(path):
#     return static_file(path, root="./")
debug(True)
run(host='localhost', port=8080, reloader=True)