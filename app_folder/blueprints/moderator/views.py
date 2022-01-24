from . import moderator
from lib.verify_login import permission_required
from flask_login import login_required
from app_folder.blueprints.users.model import Permission

@moderator.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENT)
def moderator():
    return 'Moderator field'