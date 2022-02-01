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