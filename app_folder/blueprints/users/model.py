from email.policy import default
from http import server
from numbers import Integral
from app_folder.extensions import db 
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Text
from werkzeug.security import generate_password_hash, check_password_hash
from app_folder.extensions import login_manager
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# @login_manager.user_loader
# def load_user(session_token):
#     return User.query.filter_by(session_token=session_token).first()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENT = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    default = Column(Boolean, server_default='false', index=True)
    permissions = Column(Integer)
    users = relationship('User', back_populates='role')

    @staticmethod
    def insert_roles():
        roles = {
            'User' : (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True),
            "Moderator" : (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES | Permission.MODERATE_COMMENT , False),
            'Admin' : (0xff, False)
        }

        for role in roles:
            role_instance = Role.query.filter_by(name=role).first()
            if role_instance is None:
                role_instance = Role(name=role)
                role_instance.default = roles[role][1]
                role_instance.permissions = roles[role][0]
                db.session.add(role_instance)
        db.session.commit()

    def __repr__(self) :
        return f"Role {self.name}"
            

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    surname = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    username = Column(String(), nullable=False, unique=True)
    email = Column(String(60), nullable=False, unique=True)
    password = Column(String(24), nullable=False)
    gender = Column(String(10), nullable=False)
    password_hash = Column(String(128))
    active = Column(Boolean, server_default='true', nullable=False)
    member_since = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    confirmed = Column(Boolean, server_default='f', nullable=False)

    # Experience 
    job_title = Column(String(250), nullable=True, server_default='')
    education = Column(String(100), nullable=True, server_default='')
    course = Column(String(100), nullable=True, server_default='')
    about_me = Column(Text, nullable=True, server_default='')

    # custom token 
    session_token = Column(Text, nullable=False, server_default='', unique=True)

    # relationship 
    roles_id = Column(Integer, ForeignKey('roles.id'))
    
    role = relationship('Role', back_populates='users')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            else: 
                self.role = Role.query.filter_by(default=True).first()      

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

    def generate_token_for_new_email_address(self, new_email):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        return s.dumps({'email' : self.email, 'new_email' : new_email})


    def confirm_new_email_address(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
           data = s.loads(token)
        except: 
            return False

        if data.get('email') != self.email:
            return False

        self.email = data.get('new_email')
        db.session.add(self)
        db.session.commit()
        return True

    def last_seen(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def can(self, permissions):
        if self.role is not None and (self.role.permissions & permissions) == permissions:
            return True

    def is_admin(self):
        if self.can(Permission.ADMINISTER):
            return True
        return False

    @staticmethod
    def add_admin():
        admin = User(surname='Admin', first_name='Account', password='password', 
                        email="admin@gmail.com", gender='male', confirmed=True, username='Admin123')
        db.session.add(admin)
        db.session.commit()
        print('Admin added to the successfully.')
    
    def __repr__(self):
        return f'{self.surname} {self.first_name} is created.'


class MyAnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_admin(self):
        return False