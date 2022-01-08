from flask import render_template
from app_folder.blueprints.users import user


@user.route('/profile')
def profile():
    return render_template('profile.html')