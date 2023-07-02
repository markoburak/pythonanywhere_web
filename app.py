# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def hello_world():
    return 'Hello Marko here!'

@app.route('/test')
def test():
    return 'Hello test Marko here!'

@app.route('/test2')
def test2():
    return 'Hello test Teodor here!'

@app.route("/main")
def index():
    return render_template("main_page.html")