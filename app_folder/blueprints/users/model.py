from app_folder.extensions import db 
# from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
from sqlalchemy.types import Text
from werkzeug.security import generate_password_hash, check_password_hash
from app_folder.extensions import login_manager
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
from flask import current_app, session
from app_folder.blueprints.pages.models import Post
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib
from flask import request
from lib.permissions import Permission
from lib.custom_token import serializer

# @login_manager.user_loader
# def load_user(session_token):
#     return User.query.filter_by(session_token=session_token).first()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    default = db.Column(db.Boolean, server_default='false', index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', back_populates='role')

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

class Follow(db.Model):
    """
    This Follow table serve as a relationship table between follower and followed users
    """
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    

class User(db.Model, UserMixin):
    """
    User model which inherit from db.Model, UserMixin class
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    surname = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(24), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    password_hash = db.Column(db.String(250))
    active = db.Column(db.Boolean, server_default='true', nullable=False)
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, server_default='f', nullable=False)

    # Experience 
    job_title = db.Column(db.String(250), nullable=True, server_default='')
    education = db.Column(db.String(100), nullable=True, server_default='')
    course = db.Column(db.String(100), nullable=True, server_default='')
    about_me = db.Column(db.Text, nullable=True, server_default='')
    headline = db.Column(db.Text, nullable=True, server_default='')

    # custom token 
    session_token = db.Column(db.Text, nullable=False, server_default='', unique=True)

    # relationship 
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', back_populates='users')
    posts = db.relationship(Post, backref='user', lazy='dynamic', cascade='all, delete-orphan')

    # user location 
    loaction = db.Column(db.String(100), server_default='', nullable=True)
    
    # profile view count 
    profile_view_count = db.Column(db.Integer, default=0)
    total_post_view = db.Column(db.Integer, default=0)

    # user avater
    image_avater_hash = db.Column(db.String(100), server_default='')

    followed = db.relationship('Follow', 
                    foreign_keys = [Follow.follower_id], 
                    backref=db.backref('follower', lazy='joined'),
                    lazy='dynamic',
                    cascade = 'all, delete-orphan')

    followers = db.relationship('Follow', 
                    foreign_keys = [Follow.followed_id], 
                    backref=db.backref('followed', lazy='joined'),
                    lazy='dynamic',
                    cascade = 'all, delete-orphan')
    

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            else: 
                self.role = Role.query.filter_by(default=True).first()   

        if self.email is not None and self.image_avater_hash is None:
            self.image_avater_hash = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest() 

    def is_following(self, user):
        return self.followed.filter_by(followed_id = user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id = user.id).first() is not None
    
    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)
            db.session.commit()

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id = user.id).first()
        if f : 
            db.session.delete(f)
            db.session.commit()

    def get_user_total_post_views(self):
        for post in self.posts.all():
            # print(post)
            # print(self.total_post_view, 'user total view')
            if self.total_post_view == None:
                self.total_post_view = 0
                db.session.commit()
            if post.post_view_count == None:
                self.total_post_view = 0
                db.session.commit()
            else:
                self.total_post_view += 1
                db.session.commit()
        return True
        

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
        return s.dumps({"confirm":self.id}).decode("utf-8") 

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
        return s.dumps({"confirm":self.id}).decode("utf-8")

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
        return s.dumps({'email' : self.email, 'new_email' : new_email}).decode("utf-8")


    def confirm_new_email_address(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
           data = s.loads(token)
        except: 
            return False

        if data.get('email') != self.email:
            return False

        self.email = data.get('new_email')
        self.image_avater_hash = hashlib.md5(self.email.lower()).hexdigest() 
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


    def create_avatar_image(self, s=100, r='g', d="retro"):
        if request.is_secure:
            url = 'https://www.gravatar.com/avatar'
        else:
            url = "http://www.gravatar.com/avatar"

        if self.image_avater_hash:
            hash = self.image_avater_hash
        else: 
            hash = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest() 

        return f'{url}/{hash}?s={s}&r={r}&d={d}'

    @staticmethod
    def add_users(count=100):
        from sqlalchemy.exc import IntegrityError
        import random
        import forgery_py

        random.seed()
        for num in range(0,100):
            username = forgery_py.internet.user_name()
            password = forgery_py.basic.password()
            user = User(
                username = username,
                first_name = forgery_py.internet.first_name(),
                surname = forgery_py.name.last_name(),
                email = forgery_py.email.address(),
                password = password,
                gender = forgery_py.personal.gender().lower(),
                member_since    = forgery_py.date.date(),
                confirmed = random.choice([True, False]),
                job_title = forgery_py.name.job_title(),
                about_me = forgery_py.lorem_ipsum.sentence(),
                session_token = serializer().dumps([username, password]),
                loaction = forgery_py.name.location()
            )
            db.session.add(user)

            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

# Anonymous class

class MyAnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_admin(self):
        return False

    
    def create_avatar_image(self, s=None):
        return  "http://www.gravatar.com/avatar/00000000000000000000000000000000?d=robohash"

