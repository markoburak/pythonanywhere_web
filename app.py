# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, url_for, redirect


app = Flask(__name__)
app.config["DEBUG"] = True

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