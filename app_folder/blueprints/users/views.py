from os import abort
from flask import redirect, render_template, request, url_for, flash 
from app_folder.blueprints.users import user
from app_folder.blueprints.users.model import User
from flask_login import login_required, current_user
from app_folder.blueprints.users.forms import UpdateCredentials
from app_folder.extensions import db 
from flask import abort


@user.route('/profile/<string:username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)    
    return render_template('profile.html', user=user)

@user.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = UpdateCredentials()
    if form.validate_on_submit():
        current_user.password = form.password.data
        current_user.email = form.email.data
        current_user.course = form.course.data
        current_user.eductaion = form.education.data
        current_user.about_me = form.about_me.data
        current_user.date_of_birth  = form.about_me.data
        current_user.password = form.new_password.data
        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('user.profile', username=current_user.username))
    form.surname.data = current_user.surname
    form.username.data = current_user.username
    form.name.data = current_user.first_name
    form.password.data = "hoifhewoihihflqe"
    form.email.data = current_user.email
    form.course.data = current_user.course
    form.education.data = current_user.education
    form.about_me.data = current_user.about_me
    return render_template('settings.html', form=form)
