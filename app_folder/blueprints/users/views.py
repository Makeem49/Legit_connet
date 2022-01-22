from flask import redirect, render_template, url_for, flash 
from app_folder.blueprints.users import user
from flask_login import login_required, current_user
from app_folder.blueprints.users.forms import UpdateCredentials
from app_folder.extensions import db 



@user.route('/profile')
def profile():
    return render_template('profile.html')

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
        current_user.username = form.username.data
        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('user.profile'))
    form.surname.data = current_user.surname
    form.name.data = current_user.first_name
    form.username.data = current_user.username
    form.password.data = "hoifhewoihihflqe"
    form.email.data = current_user.email
    form.course.data = current_user.course
    form.education.data = current_user.education
    form.about_me.data = current_user.about_me
    return render_template('settings.html', form=form)
