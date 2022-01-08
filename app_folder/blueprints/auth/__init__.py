from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth')

from app_folder.blueprints.auth import views

