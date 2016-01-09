from bottle import route, run, template, static_file, debug

@route('/graphs')
def root():
    return template("hcExamples")

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