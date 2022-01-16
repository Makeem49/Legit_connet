from tests.conftest import client

from flask import url_for

# def login(client, email, password):
#     # function to send user data to sign in
#     return client.post(url_for("auth.login"), data={"email":email, 'password': password}, follow_redirects=True)
    

# def logout():
#     pass

def login(client, email, password):
    return client.post(url_for('auth.login'), data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get(url_for('auth.logout'), follow_redirects=True)


def register(client, surname, first_name, password, email , gender):
    new_user = {
        "surname" : surname,
        'first_name' : first_name,
        "password" : password,
        "email" :  email,
        "gender" : gender
    }
    return client.post(url_for('auth.register'), data = new_user, follow_redirects=True)
