# from app_folder.extensions import db
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
    primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
    primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String())

    followed = db.relationship('Follow',
                    foreign_keys=[Follow.follower_id],
                    backref=db.backref('follower', lazy='joined'),
                    lazy='dynamic',
                    cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                    foreign_keys=[Follow.followed_id],
                    backref=db.backref('followed', lazy='joined'),
                    lazy='dynamic',
                    cascade='all, delete-orphan')
