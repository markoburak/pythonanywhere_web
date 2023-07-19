from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

import website.config as config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # local for testing purposes
    # using local default mysql connection with specified db(already created)
    local = False
    if local:
        db_host = config.db_host_local
        db_name = config.db_name_local
        db_user = config.db_user_local
        db_password = config.db_password_local
    # connect to hosting server db
    else:
        app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
        db_host = config.db_host
        db_name = config.db_name
        db_user = config.db_user
        db_password = config.db_password

    # set DB_URI, connect to local DB or hosting DB
    if local:
        SQLALCHEMY_DATABASE_URI = f"mysql://{db_user}:{db_password}@{db_host}/{db_name}"
    else:
        SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
            username=db_user,
            password=db_password,
            hostname=db_host,
            databasename=db_name,
        )
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)

    from . import models

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    if local:
        create_database(app)

    return app
def create_database(app):
    with app.app_context():
        db.create_all()
        print('Created Database!')