from crypt import methods
from os import abort
from flask import redirect, render_template, request, url_for, flash , current_app
from app_folder.blueprints.users import user
from app_folder.blueprints.users.model import User
from flask_login import login_required, current_user
from app_folder.blueprints.users.forms import UpdateCredentials
from app_folder.extensions import db 
from flask import abort
from app_folder.blueprints.pages.models import Post
from lib.permissions import Permission
from .forms import EditPostForm


@user.route('/profile/<string:username>')
def profile(username):
    page = request.args.get('page', 1, int)
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)    
    pagination = Post.query.filter_by(user=user).order_by(Post.date_posted.desc()).paginate(page, current_app.config['LEGIT_POST_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('profile.html', user=user, posts=posts, pagination=pagination)


@user.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = UpdateCredentials()
    if form.validate_on_submit():
        current_user.password = form.password.data
        current_user.email = form.email.data
        current_user.course = form.course.data
        current_user.education = form.education.data
        current_user.about_me = form.about_me.data
        current_user.surname = form.surname.data
        current_user.first_name = form.first_name.data
        current_user.headline = form.headline.data
        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('user.profile', username=current_user.username))
    form.surname.data = current_user.surname
    form.username.data = current_user.username
    form.first_name.data = current_user.first_name
    form.email.data = current_user.email
    form.course.data = current_user.course
    form.education.data = current_user.education
    form.about_me.data = current_user.about_me
    form.headline.data = current_user.headline
    return render_template('settings.html', form=form)


@user.route('/post/<int:id>')
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])

@user.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.user and not current_user.can(Permission.WRITE_ARTICLES):
        abort(404)
    form = EditPostForm()
    if form.validate_on_submit():
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('user.post', id=post.id))
    form.content.data = post.content
    return render_template('edit_post.html', form=form, post=post)
