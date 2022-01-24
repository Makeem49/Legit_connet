from app_folder.blueprints.admin import admin
from app_folder.blueprints.auth.views import login
from lib.verify_login import admin_required, admin_only
from flask_login import login_required

@admin.route('/admin_page', methods=['GET', 'POST'])
@login_required
@admin_only
def admin_page():
    return 'This is admin page'


