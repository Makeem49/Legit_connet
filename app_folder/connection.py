from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String





engine = create_engine("postgresql://makeem49:Olayinka1?@localhost/legit_connet", echo=True, connect_args={"check_same_thread" : False})



Base = declarative_base()


Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

session  = Session()

class DataSession():

    def __init__(self, engine):
        self.engine = engine

    def create_all(self):
        Base.metadata.create_all(self.engine)

    def drop_all(self):
        Base.metadata.drop_all(bind=self.engine)

    def add(self, name):
        session.add(self, name)

    def add_all(self, lists):
        session.add_all(lists)
    
    def dirty(self):
        session.dirty()

    def rollback(self):
        session.rollback()

    def commit(self):
        session.commit()








