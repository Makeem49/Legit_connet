import os
from app_folder.app import create_app
from app_folder.blueprints.users.model import User, Role
from app_folder.blueprints.pages.models import Post, Keyword,post_keywords
from app_folder.extensions import db 
from flask_migrate import Migrate
from app_folder.tasks import celery
from app_folder.blueprints.users.model import Permission
from lib.permissions import Permission


app = create_app(celery=celery)

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, User=User, db=db, Role=Role, Post=Post, Keyword=Keyword, post_keywords=post_keywords, Permission=Permission)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')