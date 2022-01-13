from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_mail import Mail


db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()
mail = Mail()


