import os
from app_folder.app import create_app
from app_folder.blueprints.users.model import User
from app_folder.extensions import db 
from flask_migrate import Migrate
from app_folder.tasks import celery


app = create_app(celery=celery)

migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, User=User, db=db)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')