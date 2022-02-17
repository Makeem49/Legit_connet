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

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    date_posted = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey('users.id'))
    keywords = relationship('Keyword', secondary=post_keywords, back_populates='posts', lazy='dynamic') # Post_instance.keywords will return a list which you can  append a keywords to it e.g post.keywords.append(Keyword(name='wolrd'))
    
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


class Keyword(db.Model):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)

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

    name = Column(Enum(*Hash_Tag, name='hash_tag', native_enum=False,  validate_strings = True), index=True, nullable=False, server_default='all')
    posts = relationship(Post, secondary=post_keywords, back_populates='keywords', lazy='dynamic') #Keywords_instance.posts will return a list which you can  append a post to it e.g keyword.post.append(Post(post='lorem', author=author))
