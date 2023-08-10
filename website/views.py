from flask import Blueprint, render_template, request, redirect, url_for
from .models import Comment, User_testing
from . import db

views = Blueprint('views', __name__)

@views.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        comments = Comment.query.all()
        return render_template("main.html", comments=comments)
    elif request.method == "POST":
        new_comment = Comment(content=request.form["contents"])
        db.session.add(new_comment)
        db.session.commit()
    return redirect(url_for('views.index'))

@views.route("/user_info_all", methods=["GET"])
def user_info_all():
    if request.method == "GET":
        user_info_all = User_testing.query.all()
        return render_template("user_info_all.html", user_info_all=user_info_all)
@views.route("/user_info/<user_id>", methods=["GET", "POST"])
def user_info(user_id):
    user_info_data = User_testing.query.filter_by(id=user_id).first()
    if request.method == "GET":
        return render_template("user_info.html", user_info=user_info_data)
    elif request.method == "POST":
        user_info_data.name = request.form["name"]
        user_info_data.lastname = request.form["lastname"]
        user_info_data.email = request.form["email"]
        user_info_data.age = request.form["age"]
        try:
            db.session.commit()
            return render_template("user_info.html", user_info=user_info_data)
        except:
            return redirect(url_for('views.user_info'))

@views.route("/user_info_delete/<user_id>", methods=["POST"])
def user_info_delete(user_id):
    if request.method == "POST":
        user_info_data = User_testing.query.filter_by(id=user_id).first()
        try:
            db.session.delete(user_info_data)
            db.session.commit()
            return redirect(url_for('views.user_info_all'))
        except:
            return redirect(url_for('views.index'))