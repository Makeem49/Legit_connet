from flask import render_template, request, g
from app_folder.blueprints.pages import page
from app_folder.blueprints.users.model import User


@page.before_request
def get_current_blueprint():
    g.name = request.endpoint
    g.active = 'active'

@page.route('/')
@page.route('/home')
def home():
    user = User.query.first()
    return render_template('home.html', user=user)
    
