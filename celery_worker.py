# from app_folder import make_celery
from app_folder.app import create_app
from app_folder import celery
from app_folder.celery_utils import init_celery

app = create_app()

init_celery(celery, app)