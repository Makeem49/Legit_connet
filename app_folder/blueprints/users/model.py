from app_folder.extensions import db 
from sqlalchemy import Column, Integer, String



class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    surname = Column(String(50))
    first_name = Column(String(50))
    email = Column(String)
    password = Column(String)

    def __repr__(self):
        return f'{self.surname} {self.first_name} is created'




