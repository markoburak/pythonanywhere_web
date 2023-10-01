from flask import Blueprint, render_template, request, redirect, url_for, flash
from website.models import User, User_lnk, User_testing, ShoppingList
from website import db
from sqlalchemy import text
from flask_login import login_required, current_user
import re

views = Blueprint('views', __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        user_shopping_list = ShoppingList.query.filter(ShoppingList.user_id == current_user.id).all()
        categories = db.session.query(ShoppingList.category).distinct().filter(ShoppingList.user_id == current_user.id).all()
        users = User.query.all()
        return render_template("main.html", shopping_list=user_shopping_list, users=users, user=current_user, categories=categories)
    return redirect(url_for('views.index'))

@views.route("/add_item", methods=["POST"])
@login_required
def add_item():
    if request.method == "POST":
        item = request.form.get('item')
        categoty = request.form.get('category')

        existing_item = ShoppingList.query.filter(ShoppingList.item == item, ShoppingList.user_id == current_user.id).first()
        if existing_item:
            flash('Item already exists.', category='error')
        elif len(item) < 3:
            flash('Item must be at least 3 characters.', category='error')
        elif len(categoty) < 3:
            flash('Category must be at least 3 characters.', category='error')
        else:
            new_item = ShoppingList(item=item, category=categoty, user_id=current_user.id)
            db.session.add(new_item)
            db.session.commit()
            flash('Item added!', category='success')

    return redirect(url_for('views.index'))

@views.route("/user_info_all", methods=["GET"])
def user_info_all():
    if request.method == "GET":
        user_info_all = User_testing.query.all()
        return render_template("user_info_all.html", user_info_all=user_info_all, user=current_user)
@views.route("/user_info/<user_id>", methods=["GET", "POST"])
def user_info(user_id):
    user_info_data = User_testing.query.filter_by(id=user_id).first()
    if request.method == "GET":
        return render_template("user_info.html", user_info=user_info_data, user=current_user)
    elif request.method == "POST":
        user_info_data.name = request.form["name"]
        user_info_data.lastname = request.form["lastname"]
        user_info_data.email = request.form["email"]
        user_info_data.age = request.form["age"]
        try:
            db.session.commit()
            return render_template("user_info.html", user_info=user_info_data, user=current_user)
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

@views.route("/user_details", methods=["GET", "POST"])
@login_required
def user_details():
    if request.method == "GET":
        linked_users = User_lnk.query.join(User, User_lnk.user_lnk_id == User.id).add_columns(User.first_name, User.email, User.code).filter(User_lnk.user_main_id == current_user.id).all()
        # with db.engine.connect() as connection:
        #     result = connection.execute(text("Select * from user_lnk join user on user_lnk.user_lnk_id = user.id  where user_lnk.user_main_id = 1;"))
        #     print(result.mappings().all())
        return render_template("user_details.html", user=current_user, linked_users=linked_users)
    elif request.method == "POST":
        user_data = User.query.filter_by(id=current_user.id).first()
        if user_data:
            user_data.first_name = request.form["first_name"]
            user_data.last_name = request.form["last_name"]
            user_data.email = request.form["email"]
            if not request.form["first_name"]:
                flash('First name must be at least 1 character', category='error')
            elif not request.form["last_name"]:
                flash('Last name must be at least 1 character', category='error')
            elif len(request.form["email"]) < 4:
                flash('Email must be greater than 3 characters.', category='error')
            else:
                try:
                    db.session.commit()
                    flash('Updated user data!', category='success')
                except:
                    flash('Something didn\'t work', category='error')
        else:
            flash('Cannot update the user!', category='error')
        return redirect(url_for('views.user_details'))


@views.route("/link_user", methods=["POST"])
@login_required
def link_user():
    if request.method == "POST":
        link_code = request.form.get('link_code')
        # make sure user enters correct data
        if not re.match("^([0-9]{4})+([a-z]{4})+$", link_code):
            flash('Wrong code', category='error')
        # check not to use user's own code
        elif link_code == current_user.code:
            flash('User cannot use his/her own code;', category='error')
        else:
            # make sure that user doesn't have the link already
            linked_user = User_lnk.query.join(User, User_lnk.user_lnk_id == User.id).add_columns(User.code).filter(User_lnk.user_main_id == current_user.id, User.code == str(link_code)).first()
            if linked_user:
                flash('User is already linked!', category='error')
            else:
                user_by_code = User.query.filter_by(code=link_code).first()
                if not user_by_code:
                    flash('Couldn\'t link the user, code didn\'t match!', category='error')
                else:
                    new_link = User_lnk(user_main_id=current_user.id, user_lnk_id=user_by_code.id)
                    db.session.add(new_link)
                    db.session.commit()
                    flash('User was successfully linked!', category='success')
        return redirect(url_for('views.user_details'))


@views.route("/delete_link/<link_id>", methods=["POST"])
@login_required
def delete_link(link_id):
    if request.method == "POST":
        link_data = User_lnk.query.filter_by(id=link_id).first()
        if not link_data:
            flash('Cannot delete the link, please contact us!', category='error')
        else:
            try:
                db.session.delete(link_data)
                db.session.commit()
                flash('Link was deleted 😊', category='success')
            except:
                flash('There was an error deleting the link, please contact us!', category='error')
        return redirect(url_for('views.user_details'))