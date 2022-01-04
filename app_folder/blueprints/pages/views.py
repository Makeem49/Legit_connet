from flask import render_template
from app_folder.blueprints.pages import page

@page.route('/')
@page.route('/home')
def home():
    login = None
    return render_template('home.html', login=login)
    