from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_moment import Moment



login_manager = LoginManager()
db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()
mail = Mail()
moment = Moment()
