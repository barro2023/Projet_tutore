from app import db
from flask_login import UserMixin
#from flask_sqlalchemy import SQLAlchemy
#from flask_login import UserMixin
#db = SQLAlchemy()

class SearchPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text())
    price = db.Column(db.Integer)
    location = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    preferences = db.relationship('SearchPreferences', backref='user', lazy=True)

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text())
    price = db.Column(db.Integer)
    location = db.Column(db.String(255))
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
        
