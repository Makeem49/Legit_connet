import sqlite3
from app_folder.blueprints import users
from tests.auth.utils_login import login, logout
from flask import url_for, current_app
from app_folder.blueprints.users.model import User
import re

class TestLoginLogout(object):
    def test_login_page(self, client):
        # test login page get request 
        response = client.get(url_for("auth.login"))
        assert response.status_code == 200

    def test_message_login(self, client, users):
        response = login(client, 'admin@gmail.com', 'password')
        assert response.status_code == 200

    # def test_logout_page(self, client, users):
    #     response = logout(client)
    #     # assert response.status_code == 200
    #     assert b"You have successfully logout" in response.data

    def test_login_logout(self, client, users):
        response = login(client, 'admin@gmail.com', 'password')
        assert response.status_code == 200

        # response = logout(client)
        # assert b"You have successfully logout" in response.data

        response = login(client, 'admin@gmail.com', 'password')
        assert response.status_code == 200
    



class TextConfig(object):
    def test_config(self, app):
        with app.test_request_context():
            assert current_app.config['TESTING'] == True

    def test_database(self, app):
        with app.test_request_context():
            assert current_app.config['SQLALCHEMY_DATABASE_URI']  is "app_folder/test.sqlite"


class Test_Register(object):
    def test_register_page(self, client):
        response = client.get(url_for('auth.register'))
        assert response.status_code == 200

    def test_sign_up(self, client, users):
        user = {
            "surname" : 'pop',
            'first_name' : "lollu",
            "password" : 'password',
            "email" :  "pop@gmail.com",
            "gender" : 'female'
         }
        response = client.post(url_for('auth.register'), data=user , follow_redirects=True)
        assert response.status_code == 200

    def test_user_count(self, users):
        user_queery = User.query.count()
        # assert "pop" in user_queery
        assert user_queery == 2

    

