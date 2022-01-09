from flask_wtf.csrf import CSRFError
from app_folder.blueprints.error import error
from flask import render_template

@error.app_errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400

@error.app_errorhandler
def page_not_found(e):
    return render_template('page_not_found.html', reason=e.description), 404

@error.app_errorhandler
def handle_csrf_error(e):
    return render_template('server_down.html', reason=e.description), 500