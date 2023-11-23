from flask import Blueprint, render_template, request, redirect, url_for, flash
from website.models import User, User_lnk, ShoppingList, User_admin
from website import db
from sqlalchemy import or_
from flask_login import login_required, current_user
import re

views = Blueprint('views', __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":

        linked_users = [x.user_lnk_id for x in User_lnk.query.filter(User_lnk.user_main_id == current_user.id).all()]

        user_shopping_list = ShoppingList.query.filter(ShoppingList.active == True).filter(
            or_(ShoppingList.user_id == current_user.id, ShoppingList.user_id.in_(linked_users))).all()

        categories = db.session.query(ShoppingList.category).distinct().filter(ShoppingList.active == True).filter(
            or_(ShoppingList.user_id == current_user.id, ShoppingList.user_id.in_(linked_users))).all()
        users = User.query.all()
        admin_user = User_admin.query.filter(User_admin.user_id == current_user.id, User_admin.active == 1).first()
        if admin_user:
            return redirect(url_for('admin.admin_home'))
        return render_template("main.html", shopping_list=user_shopping_list, users=users, user=current_user, categories=categories, admin_user=admin_user)
    return redirect(url_for('views.index'))

@views.route("/add_item", methods=["POST"])
@login_required
def add_item():
    if request.method == "POST":
        item = request.form.get('item_modal')
        categoty = request.form.get('category_modal')

        existing_item = ShoppingList.query.filter(ShoppingList.item == item, ShoppingList.active == True, ShoppingList.user_id == current_user.id).first()
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

@views.route("/update_item_checkbox/<item_id>", methods=["POST"])
@login_required
def update_item_checkbox(item_id):
    if request.method == "POST":
        checkbox_checked = False
        if request.form.get("checkbox_to_update"):
            checkbox_checked = True

        existing_item = ShoppingList.query.filter(ShoppingList.id == item_id, ShoppingList.active == True).first()
        if existing_item:
            existing_item.checked = checkbox_checked
            try:
                db.session.commit()
            except:
                flash('Couldn\'t update the item', category='error')
        else:
            flash('Cannot find the item!', category='error')
        return redirect(url_for('views.index'))

@views.route("/delete_checked", methods=["POST"])
@login_required
def delete_checked():
    if request.method == "POST":
        linked_users = [x.user_lnk_id for x in User_lnk.query.filter(User_lnk.user_main_id == current_user.id).all()]

        items = ShoppingList.query.filter(ShoppingList.checked == True, ShoppingList.active == True).filter(
            or_(ShoppingList.user_id == current_user.id, ShoppingList.user_id.in_(linked_users))).all()
        if items:
            for item in items:
                item.active = False
            try:
                db.session.commit()
                flash('Deleted checked items!', category='success')
            except:
                flash('Couldn\'t delete the items', category='error')
        return redirect(url_for('views.index'))

