from flask import Blueprint, render_template, request, redirect, url_for, flash
from website.models import User, User_lnk, User_admin
from website import db
from flask_login import login_required, current_user
import re

user_details_bp = Blueprint('user_details_bp', __name__)

@user_details_bp.route("/user_details", methods=["GET", "POST"])
@login_required
def user_details():
    if request.method == "GET":
        linked_users = User_lnk.query.join(User, User_lnk.user_lnk_id == User.id).add_columns(User.first_name, User.email, User.code).filter(User_lnk.user_main_id == current_user.id).all()
        admin_user = User_admin.query.filter(User_admin.user_id == current_user.id, User_admin.active == 1).first()
        return render_template("user_details.html", user=current_user, linked_users=linked_users, admin_user=admin_user)
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
        return redirect(url_for('user_details_bp.user_details'))


@user_details_bp.route("/update_dark_mode", methods=["POST"])
@login_required
def update_dark_mode():
    if request.method == "POST":
        user_data = User.query.filter_by(id=current_user.id).first()
        if user_data:
            dark_mode_toggle = False
            if request.form.get("dark_mode_toggle"):
                dark_mode_toggle = True
            user_data.dark_mode = dark_mode_toggle
            try:
                db.session.commit()
                # flash('Updated item!', category='success')
            except:
                flash('Couldn\'t update the item', category='error')
        else:
            flash('Cannot find the item!', category='error')
    return redirect(url_for('user_details_bp.user_details'))

@user_details_bp.route("/link_user", methods=["POST"])
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
        return redirect(url_for('user_details_bp.user_details'))


@user_details_bp.route("/delete_link/<link_id>", methods=["POST"])
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
        return redirect(url_for('user_details_bp.user_details'))
