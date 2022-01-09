from flask import Blueprint

error = Blueprint('error', __name__, template_folder='templates')

from app_folder.blueprints.error import views

