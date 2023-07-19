from flask import Blueprint, render_template, request, redirect, url_for
from .models import Comment
from . import db

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

@views.route("/main", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        comments = Comment.query.all()
        return render_template("main.html", comments=comments)
    elif request.method == "POST":
        new_comment = Comment(content=request.form["contents"])
        db.session.add(new_comment)
        db.session.commit()
    return redirect(url_for('views.index'))