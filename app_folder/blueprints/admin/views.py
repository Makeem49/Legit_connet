from crypt import methods

from flask import flash, redirect, render_template, url_for
from app_folder.blueprints.admin import admin
from app_folder.blueprints.auth.views import login
from lib.verify_login import admin_required, admin_only
from flask_login import login_required
from .forms import AdminEditUserForm
from app_folder.blueprints.users.model import User
from app_folder.extensions import db

@admin.route('/admin_page')
@login_required
@admin_only
def admin_page():
    users = User.query.all()
    return render_template('admin-users.html', users = users)

@admin.route('/edit-user/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_only
def admin_edit_user(id):
    user = User.query.get_or_404(id)
    form = AdminEditUserForm(user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.gender= form.gender.data
        user.confirmed = form.confirmed.data
        user.active = form.active.data
        user.memeber_since = form.member_since.data
        user.job_title = form.job_title.data
        user.education = form.education.data
        user.course = form.course.data
        user.role_id = form.role.data
        flash('{user.username} profile updated')
        return redirect(url_for('admin.admin_edit_user'))
    form.email.data = user.email 
    form.username.data = user.username 
    form.first_name.data = user.first_name 
    form.last_name.data = user.last_name 
    form.gender.data = user.gender
    form.confirmed.data =  user.confirmed 
    form.active.data = user.active 
    form.member_since.data = user.memeber_since
    form.job_title.data = user.job_title 
    form.education.data = user.education 
    form.course.data = user.course 
    form.role.data =  user.role_id
    return render_template('edit-user.html', form=form)
    

