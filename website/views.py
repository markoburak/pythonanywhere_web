from flask import Blueprint, render_template, request, redirect, url_for

views = Blueprint('views', __name__)

@views.route("/")
def hello_world():
    return 'Hello Marko here!'

@views.route('/test')
def test():
    return 'Hello test Marko here!'

@views.route('/test2')
def test2():
    return 'Hello test Teodor here!'

comments = []
@views.route("/main", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main.html", comments=comments)
    elif request.method == "POST":
        comments.append(request.form["contents"])
    return redirect(url_for('views.index'))