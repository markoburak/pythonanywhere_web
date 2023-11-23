from flask import Blueprint, render_template, request, redirect, url_for, flash
from website.models import User, ShoppingList, User_lnk
from website import db
from sqlalchemy import or_
from flask_login import login_required, current_user

item_details_bp = Blueprint('item_details_bp', __name__)

@item_details_bp.route("/item_details/<item_id>", methods=["GET", "POST"])
@login_required
def item_details(item_id):
    if request.method == "GET":
        item_info = ShoppingList.query.filter_by(id=item_id).first()
        if item_info:
            item_user = User.query.filter_by(id=item_info.user_id).first()

            linked_users = [x.user_lnk_id for x in
                            User_lnk.query.filter(User_lnk.user_main_id == current_user.id).all()]
            categories = db.session.query(ShoppingList.category).distinct().filter(ShoppingList.active == True).filter(
                or_(ShoppingList.user_id == current_user.id, ShoppingList.user_id.in_(linked_users))).all()
            return render_template("item_details.html", user=current_user, item_info=item_info, item_user=item_user, categories=categories)
        else:
            return redirect(url_for('views.index'))
    elif request.method == "POST":

        item_info = ShoppingList.query.filter_by(id=item_id).first()
        if item_info:
            new_name = request.form["item_name"]
            new_category = request.form["item_category"]
            try:
                _ = request.form["item_checked"]
            except:
                new_checked = False
            else:
                new_checked = True
            if len(new_name) < 3:
                flash('Item must be at least 3 characters.', category='error')
            elif len(new_category) < 3:
                flash('Category must be at least 3 characters.', category='error')
            else:

                item_info.item = new_name
                item_info.category = new_category
                item_info.checked = new_checked

                try:
                    db.session.commit()
                    flash('Item updated!', category='success')
                except:
                    flash('Something didn\'t work', category='error')
        else:
            flash('Cannot update the item!', category='error')
        return redirect(url_for('views.index'))
