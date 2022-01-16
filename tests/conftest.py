import pytest 
from app_folder.app import create_app
from app_folder.blueprints.users.model import User
from app_folder.extensions import db as _db
import os

@pytest.fixture(scope='session')
def app():
    # creating app factory for testing

    params = {
        "TESTING" : True,
        "DEBUG" : False,
        "WTF_CSRF_ENABLED" : False
    }

    _app = create_app(params)
    print(_app)

    ctx = _app.app_context()

    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def client(app):
    # creating a fake request for testing
    with app.test_client() as client:
        yield client



@pytest.fixture(scope='session')
def db(app):
    # create a database for testing 
    _db.drop_all() # Destroying the table user per session 
    _db.create_all() # creating a new table per user session 

    param = {
        "surname" : "John",
        "first_name" : "Doe",
        "email" : "admin@gmail.com",
        "password" : "password",
        "gender" : "male"
    }

    user = User(**param)

    _db.session.add(user)
    _db.session.commit()

    return _db 

@pytest.fixture()
def session():

    # it help allow for fast testing using sessionn and rolback 
    db.session.begin_nested

    yield db.session

    db.session.rollback()


@pytest.fixture(scope='function')
def users(db):
    # Load users in the test database perfunction

    db.session.query(User).delete()

    users = [
        {
            "surname" : 'pop',
            'first_name' : "lollu",
            "password" : 'password',
            "email" :  "pop@gmail.com",
            "gender" : 'female'
         },
         {
            "surname" : 'John',
            'first_name' : "Camp",
            "password" : 'password',
            "email" :  "John@gmail.com",
            "gender" : 'male'
         }
    ]

    for user in users:
        db.session.add(User(**user))
    db.session.commit()

    return db