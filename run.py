import os
from app_folder import create_app
from app_folder.blueprints.users.model import User
from app_folder.extensions import db 


app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, User=User, db=db)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')