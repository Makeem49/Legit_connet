from flask import render_template
from app_folder.blueprints.users import user

@user.route('/login')
def login():
    return render_template('login.html')