from http import server
from app_folder.extensions import db 
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.types import Text
from werkzeug.security import generate_password_hash, check_password_hash
from app_folder.extensions import login_manager
from flask_login import UserMixin
from datetime import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


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
    active = Column(Boolean, server_default='true', nullable=False)
    last_seen = Column(DateTime, default=datetime.utcnow)
    confirmed = Column(Boolean, server_default='f', nullable=False)

    job_title = Column(String(250), nullable=True, server_default='')

    # custom token 
    session_token = Column(Text, nullable=False, server_default='', unique=True)


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

    def generate_confirmation_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        return s.dumps({"confirm":self.id})

    def confirm_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
           data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True
    
    
    def generate_password_rest_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        return s.dumps({"confirm":self.id})

    @staticmethod
    def confirm_password_reset_token(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
           data = s.loads(token)
           print(f"{data} {new_password} is generated")
        except:
            return False
        user = User.query.get(int(data.get('confirm')))
        print(f"{user} is now created")
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        db.session.commit()
        return True


    def __repr__(self):
        return f'{self.surname} {self.first_name} is created.'

        


    



