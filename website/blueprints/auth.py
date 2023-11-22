import random, string
from flask import Blueprint, render_template, request, redirect, url_for, flash
from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for(('views.index')))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def generate_unique_code():
    return str(random.randrange(1000, 10000)) + ''.join([random.choice(string.ascii_lowercase) for _ in range(4)])

def create_unique_code(num_of_run):
    unique_code = generate_unique_code()
    user_exists = User.query.filter_by(code=unique_code).first()
    if num_of_run > 5:
        return ""
    elif user_exists:
        num_of_run += 1
        create_unique_code(num_of_run)
    else:
        return unique_code

@auth.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Password don\'t match', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 7 characters', category='error')
        else:

            unique_code = create_unique_code(0)
            if not unique_code:
                flash('Code couldn\'t be generated. Contact us, please.', category='error')
            else:
                new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='sha256'), code=unique_code)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.index'))

    return render_template("sign_up.html", user=current_user)