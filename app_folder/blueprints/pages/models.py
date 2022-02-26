from sqlalchemy import Column, ForeignKey, DateTime, Integer, String, Table
from sqlalchemy.types import Text, Enum
from sqlalchemy.orm import relationship
from app_folder.extensions import db 
from datetime import datetime
from collections import OrderedDict
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


post_keywords = db.Table('post_keywords', 
    db.Column('keyword_id', db.Integer, db.ForeignKey('keywords.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
    )

# Post model 
class Post(db.Model):
    __tablename__  = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    keywords = db.relationship('Keyword', secondary=post_keywords, back_populates='posts', lazy='dynamic') # Post_instance.keywords will return a list which you can  append a keywords to it e.g post.keywords.append(Keyword(name='wolrd'))
    
    # post view count 
    post_view_count = Column(Integer, default=0)

    # user = relationship('User', back_populates='posts')

    @staticmethod
    def add_post(count=100):
        from random import seed, randint
        import forgery_py

        from app_folder.blueprints.users.model import User
        seed()
        user_count = User.query.count()
        for num in range(0,100):
            user = User.query.offset(randint(0, user_count-1)).first()
            post = Post(content = forgery_py.lorem_ipsum.paragraphs(), date_posted=forgery_py.date.date(True), user = user)
            db.session.add(post)
            db.session.commit()
    
    def get_total_post_view(self):
        if self.post_view_count == None:
            self.post_view_count = 0
            db.session.commit()
        else:
            self.post_view_count += 1
        db.session.commit()
        return self.post_view_count

class Keyword(db.Model):
    __tablename__ = 'keywords'
    id = db.Column(db.Integer, primary_key=True)

    Hash_Tag = OrderedDict([
        ('all', "All"),
        ("world", "World"),
        ("u.s", "U.S"),
        ("technology", "Technology"),
        ("design", "Design"),
        ("culture", "Culture"),
        ("business", "Business"),
        ("politics", "Politics"),
        ("opinion", "Opinion"),
        ("science", "Science"),
        ("style", "Style"),
        ("travel", "Travel"),
    ])

    name = db.Column(db.Enum(*Hash_Tag, name='hash_tag', native_enum=False,  validate_strings = True), index=True, nullable=False, server_default='all')
    posts = db.relationship(Post, secondary=post_keywords, back_populates='keywords', lazy='dynamic') #Keywords_instance.posts will return a list which you can  append a post to it e.g keyword.post.append(Post(post='lorem', author=author))
