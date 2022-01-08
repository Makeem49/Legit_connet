from flask import render_template, request, g
from app_folder.blueprints.pages import page


@page.before_request
def get_current_blueprint():
    g.name = request.endpoint
    g.active = 'active'

@page.route('/')
@page.route('/home')
def home():
    login = True
    return render_template('home.html', login=login)
    
