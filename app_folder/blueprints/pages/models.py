from sqlalchemy import Column, ForeignKey, DateTime, Integer
from sqlalchemy.types import Text
from app_folder.extensions import db 
from datetime import datetime

# Post model 
class Post(db.Model):
    __tablename__  = 'posts'

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    date_posted = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey('users.id'))
    
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

