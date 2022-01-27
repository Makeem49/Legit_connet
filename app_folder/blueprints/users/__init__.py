from flask import Blueprint
from .model import Permission

user = Blueprint('user', __name__, template_folder="templates", url_prefix='/user')

from app_folder.blueprints.users import views

@user.app_context_processor
def inject_permisstion():
    return dict(Permission=Permission)