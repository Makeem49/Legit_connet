from . import post
from .forms import PostForm
from app_folder.extensions import db 
from flask import redirect , url_for

@post.route('user-post', methods=['POST'])
def user_post():
    form = PostForm()
    if form.validate_on_submit():
        content = form.content.data
        db.session.add(content)
        db.session.commit()
        return redirect(url_for('pae.home'))