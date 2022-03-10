import os

from flask import Flask
from app_folder.blueprints.pages import page
from app_folder.blueprints.users import user
from app_folder.blueprints.auth import auth
from app_folder.blueprints.error import error
from app_folder.blueprints.admin import admin
from app_folder.blueprints.error import error
from app_folder.blueprints.api_v_1_0 import api as api_v_1_blueprint
from app_folder.blueprints.moderator import moderator
from app_folder.blueprints.users.model import MyAnonymousUser

# extension 
from app_folder.extensions import db 
from app_folder.extensions import csrf
from app_folder.extensions import migrate
from app_folder.extensions import mail
from app_folder.extensions import login_manager
from app_folder.extensions import moment


from app_folder.celery_utils import init_celery


# flask_login configuration for authentication
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page'
login_manager.login_message_category = 'info'

# flask_login for fresh login if user change their password or name or any sensitive information
login_manager.refresh_view  = 'auth.login'
login_manager.needs_refresh_message = 'To make your account safe, please reauthenticate'
login_manager.needs_refresh_message_category = "info"

# flask_login session protection 
login_manager.session_protection = "strong"

# Anonymous user
login_manager.anonymous_user = MyAnonymousUser




basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(settings_override=None, **kwargs):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    if settings_override is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(settings_override)
        app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir, 'test.sqlite'), SERVER_NAME='localhost.localdomain:5000')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if kwargs.get('celery'):
        init_celery(kwargs.get('celery'), app)

    # registering blueprint
    app.register_blueprint(page)
    app.register_blueprint(user)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(moderator)
    app.register_blueprint(error)
    # app.register_blueprint(api_v_1_blueprint)

    # initialising extension
    extensions(app)

    return app


def extensions(app):
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)

