from flask import Blueprint

user = Blueprint('user', __name__, template_folder="templates", url_prefix='/user')

from app_folder.blueprints.users import views