# A very simple Flask Hello World app for you to get started with...

from models import Comment

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
db = SQLAlchemy(app)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="burakmarko",
    password="testdb123",
    hostname="burakmarko.mysql.pythonanywhere-services.com",
    databasename="burakmarko$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.route("/")
def hello_world():
    return 'Hello Marko here!'

@app.route('/test')
def test():
    return 'Hello test Marko here!'

@app.route('/test2')
def test2():
    return 'Hello test Teodor here!'

comments = []

@app.route("/main", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main.html", comments=comments)
    elif request.method == "POST":
        comments.append(request.form["contents"])
    return redirect(url_for('index'))