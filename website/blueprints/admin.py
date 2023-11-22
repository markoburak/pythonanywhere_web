from flask import Blueprint, render_template, request, redirect, url_for, flash
from website.models import User, User_lnk, ShoppingList, User_admin
from website import db
from flask_login import login_required, current_user


admin = Blueprint('admin', __name__)

# admin_shopping@admin.com
@admin.route("/", methods=["GET"])
@login_required
def admin_home():
    if request.method == "GET":
        admin_user = User_admin.query.filter(User_admin.user_id == current_user.id, User_admin.active == 1).first()
        if not admin_user:
            flash('User is not the admin!', category='error')
            return redirect(url_for('views.index'))
        else:
            # active_admins = [x.user_id for x in User_admin.query.filter(User_admin.active == 1).all()]
            all_admins = [x.user_id for x in User_admin.query.all()]

            admins = User.query.join(User_admin, User.id==User_admin.user_id).add_columns(User_admin.active).filter(User.id.in_(all_admins)).all()
            users = User.query.filter(User.id.not_in(all_admins)).all()

            return render_template("admin.html", user=current_user, admins=admins, users=users)

@admin.route("/get_list_by_user/<user_id>", methods=["GET", "POST"])
@login_required
def admin_get_list_by_user(user_id):
    if request.method == "GET":
        admin_user = User_admin.query.filter(User_admin.user_id == current_user.id, User_admin.active == 1).first()
        if not admin_user:
            flash('User is not the admin!', category='error')
            return redirect(url_for('views.index'))
        else:
            items = ShoppingList.query.filter(ShoppingList.user_id == user_id).all()
            user_email = User.query.filter(User.id == user_id).first()

            categories = db.session.query(ShoppingList.category).distinct().filter(ShoppingList.active == True).filter(ShoppingList.user_id == user_id).all()

            return render_template("list_by_user.html", user=current_user, items=items, user_email=user_email, categories=categories)

@admin.route("/update_item_by_id/<user_id>/<item_id>", methods=["POST"])
@login_required
def admin_update_item_by_id(user_id, item_id):
    if request.method == "POST":
        admin_user = User_admin.query.filter(User_admin.user_id == current_user.id, User_admin.active == 1).first()
        if not admin_user:
            flash('User is not the admin!', category='error')
            return redirect(url_for('views.index'))
        else:
            new_name = request.form.get("item_name")
            new_category = request.form.get("category")
            new_checked = request.form.get("checked")
            new_active = request.form.get("active")
            new_created_date = request.form.get("created_date")


            existing_item = ShoppingList.query.filter(ShoppingList.id == item_id).first()
            if existing_item:
                if len(new_name) < 3:
                    flash('Item must be at least 3 characters.', category='error')
                elif len(new_category) < 3:
                    flash('Category must be at least 3 characters.', category='error')
                else:
                    new_checked = 1 if new_checked else 0
                    new_active = 1 if new_active else 0

                    if new_name == existing_item.item and new_category == existing_item.category and new_checked == existing_item.checked and new_active == existing_item.active and new_created_date == existing_item.created_date:
                        flash('There is nothing to update', category='error')
                    else:
                        existing_item.item = new_name
                        existing_item.category = new_category
                        existing_item.checked = new_checked
                        existing_item.active = new_active
                        existing_item.created_date =new_created_date
                        try:
                            db.session.commit()
                            flash('Updated item!', category='success')
                        except:
                            flash('Couldn\'t update the item', category='error')
            else:
                flash('Cannot find the item!', category='error')
            return redirect(url_for('admin.admin_get_list_by_user', user_id = user_id))


@admin.route("/upgrade_user_to_admin/<user_id>", methods=["POST"])
@login_required
def admin_upgrade_user_to_admin_by_id(user_id):
    if request.method == "POST":
        admin_user = User_admin.query.filter(User_admin.user_id == current_user.id, User_admin.active == 1).first()
        if not admin_user:
            flash('User is not the admin!', category='error')
            return redirect(url_for('views.index'))
        else:

            user_to_change = User.query.filter(User.id == user_id).first()
            if user_to_change:
                try:
                    new_admin = User_admin(user_id=user_id, active=1)
                    db.session.add(new_admin)
                    db.session.commit()
                    flash(f'User {user_id} was upgraded to the admin!', category='success')
                except:
                    flash('Couldn\'t upgrade the admin', category='error')
            else:
                flash('Cannot find the user to upgrade!', category='error')
            return redirect(url_for('admin.admin_home'))


@admin.route("/downgrade_user_to_customer/<admin_id>", methods=["POST"])
@login_required
def admin_downgrade_admin_to_customer_by_id(admin_id):
    if request.method == "POST":
        admin_user = User_admin.query.filter(User_admin.user_id == current_user.id, User_admin.active == 1).first()
        if not admin_user:
            flash('User is not the admin!', category='error')
            return redirect(url_for('views.index'))
        else:
            admin_user_to_change = User_admin.query.filter(User_admin.user_id == admin_id).first()
            if admin_user_to_change:
                try:
                    db.session.delete(admin_user_to_change)
                    db.session.commit()
                    flash(f'User {admin_id} was downgraded to the customer!', category='success')
                except:
                    flash('Couldn\'t downgrade the admin', category='error')
            else:
                flash('Cannot find the user to downgrade!', category='error')
            return redirect(url_for('admin.admin_home'))

@admin.route("/activate_admin/<admin_id>", methods=["POST"])
@login_required
def admin_resume_admin_by_id(admin_id):
    if request.method == "POST":
        admin_user = User_admin.query.filter(User_admin.user_id == current_user.id, User_admin.active == 1).first()
        if not admin_user:
            flash('User is not the admin!', category='error')
            return redirect(url_for('views.index'))
        else:
            admin_user_to_change = User_admin.query.filter(User_admin.user_id == admin_id).first()
            if admin_user_to_change:
                try:
                    admin_user_to_change.active = True
                    db.session.commit()
                    flash(f'User {admin_id} was activated!', category='success')
                except:
                    flash('Couldn\'t activate the admin', category='error')
            else:
                flash('Cannot find the user to activate!', category='error')
            return redirect(url_for('admin.admin_home'))


@admin.route("/deactivate_admin/<admin_id>", methods=["POST"])
@login_required
def admin_stop_by_id(admin_id):
    if request.method == "POST":
        admin_user = User_admin.query.filter(User_admin.user_id == current_user.id, User_admin.active == 1).first()
        if not admin_user:
            flash('User is not the admin!', category='error')
            return redirect(url_for('views.index'))
        else:
            admin_user_to_change = User_admin.query.filter(User_admin.user_id == admin_id).first()
            if admin_user_to_change:
                try:
                    admin_user_to_change.active = False
                    db.session.commit()
                    flash(f'User {admin_id} was deactivated!', category='success')
                except:
                    flash('Couldn\'t deactivate the admin', category='error')
            else:
                flash('Cannot find the user to deactivate!', category='error')
            return redirect(url_for('admin.admin_home'))
