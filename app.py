# A very simple Flask Hello World app for you to get started with...

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello Marko here!'

@app.route('/test')
def test():
    return 'Hello test Marko here!'

@app.route('/test2')
def test2():
    return 'Hello test Teodor here!'