from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class ShoppingList(db.Model):

    __tablename__ = "shopping_list"

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(50))
    created_date = db.Column(db.Date(), default=func.now())
    category = db.Column(db.String(50), default='Default')
    checked = db.Column(db.Boolean, default=False, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    code = db.Column(db.String(8), unique=True)
    dark_mode = db.Column(db.Boolean, default=True, nullable=False)
    shopping_list = db.relationship('ShoppingList')
class User_lnk(db.Model, UserMixin):
    __tablename__ = "user_lnk"

    id = db.Column(db.Integer, primary_key=True)
    user_main_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_lnk_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User_admin(db.Model, UserMixin):
    __tablename__ = "user_admin"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    active = db.Column(db.Boolean, default=True, nullable=False)