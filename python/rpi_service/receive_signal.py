from flask import Flask, render_template, request

app = Flask(__name__)

FLASK_GET = None

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/getter", methods=['GET'])
def getname():
    global FLASK_GET
    FLASK_GET = name = request.args.get('name')
    match name:
        case 'Point_Up':
            
    return f"<p>received:{name}</p>"

app.run(host='localhost', port=8500)