from app_folder.extensions import db 
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from werkzeug.security import generate_password_hash, check_password_hash
from app_folder.extensions import login_manager
from flask_login import UserMixin
from datetime import datetime
from flask import current_app
import os 


# @login_manager.user_loader
# def load_user(session_token):
#     return User.query.filter_by(session_token=session_token).first()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    surname = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    username = Column(String(), nullable=True, unique=True)
    email = Column(String(60), nullable=False, unique=True)
    password = Column(String(24), nullable=False)
    gender = Column(String(10), nullable=False)
    password_hash = Column(String(128))
    active = Column(Boolean, server_default='1')
    last_seen = Column(DateTime, default=datetime.utcnow)

    job_title = Column(String(250), nullable=True, server_default='')

    # custom token 
    session_token = Column(String(250), nullable=False, server_default='', unique=True)


    @property
    def password(self):
        raise AttributeError('password is not a readable property.')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def is_active(self):
        return self.active 
    
    def __repr__(self):
        return f'{self.surname} {self.first_name} is created'

    



