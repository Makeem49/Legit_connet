import os

from flask import Flask
from app_folder.blueprints.pages import page
from app_folder.blueprints.users import user
from app_folder.blueprints.auth import auth

from app_folder.extensions import db 





def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # registering blueprint
    app.register_blueprint(page)
    app.register_blueprint(user)
    app.register_blueprint(auth)

    # initialising extension
    extensions(app)




    return app


def extensions(app):
    db.init_app(app)