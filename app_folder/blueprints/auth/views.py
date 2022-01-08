from flask import request, render_template, g, redirect, url_for
from app_folder.blueprints.auth import auth


@auth.before_request 
def get_current_blueprint():
    g.name = request.endpoint
    g.active = 'active'

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/register')
def register():
    return render_template('register.html')

@auth.route('/logout')
def logout():
    return redirect(url_for('auth.login'))