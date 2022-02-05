from crypt import methods
from traceback import print_tb
from flask import current_app, render_template, request, g, redirect , url_for
from app_folder.blueprints.pages import page
from app_folder.blueprints.users.model import User
from .forms import PostForm
from app_folder.extensions import db 
from flask_login import login_required, current_user
from .models import Post
from lib.permissions import Permission


@page.before_request
def get_current_blueprint():
    g.name = request.endpoint
    g.active = 'active'



@page.route('/', methods=['GET', 'POST'])
@page.route('/home',  methods=['GET', 'POST'])
def home():
    form = PostForm()
    page = request.args.get('page', 1 , int)
    print(request.args.get('page'))
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(content = form.content.data, user = current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('page.home'))
    pagination = Post.query.order_by(Post.date_posted.desc()).paginate(page, current_app.config['LEGIT_POST_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('home.html', posts=posts, form=form, pagination=pagination)