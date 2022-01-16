import pytest
from app_folder.blueprints.users.model import User

class TestModel(object):
    def test_password_setter(self, db):
        param = {
            "surname" : "John",
            "first_name" : "Doe",
            "email" : "admin@gmail.com",
            "password" : "password",
            "gender" : "male"
        }
        user = User(**param)
        assert user.password_hash is not None

    def test_password_not_accessible(self, db):
        param = {
            "surname" : "John",
            "first_name" : "Doe",
            "email" : "admin@gmail.com",
            "password" : "password",
            "gender" : "male"
        }
        user = User(**param)
        with pytest.raises(AttributeError):
            user.password
        

    def test_password_hash_is_random(self, db):
        param = {
            "surname" : "John",
            "first_name" : "Doe",
            "email" : "admin@gmail.com",
            "password" : "password",
            "gender" : "male"
        }
        user = User(**param)
        user1 = User(**param)
        assert user.password_hash != user1.password_hash

    def test_password_cannot_compare(self, db):
        param = {
            "surname" : "John",
            "first_name" : "Doe",
            "email" : "admin@gmail.com",
            "password" : "password",
            "gender" : "male"
        }
        user = User(**param)
        assert user.verify_password('password') == True


        