from flask import render_template, request, g
from app_folder.blueprints.users import user

@user.before_request 
def get_current_blueprint():
    g.name = request.endpoint
    g.active = 'active'

@user.route('/login')
def login():
    return render_template('login.html')


@user.route('/logout')
def logout():
    return render_template('logout.html')