from . import db

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))


class User_testing(db.Model):
    __tablename__ = "user_testing"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))
    lastname = db.Column(db.String(512))
    email = db.Column(db.String(512))
    age = db.Column(db.Integer())
