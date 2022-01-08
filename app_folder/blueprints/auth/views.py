from flask import request, render_template, g, redirect, url_for
from app_folder.blueprints.auth import auth
from app_folder.blueprints.users.forms import RegisterForm
from app_folder.blueprints.users.model import User
from app_folder.extensions import db



@auth.before_request 
def get_current_blueprint():
    g.name = request.endpoint
    g.active = 'active'

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user is None:
            surname = form.surname.data
            first_name = form.first_name.data
            email = form.email.data
            password = form.password.data
            user = User(surname=surname, first_name=first_name, email=email, passowrd=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/logout')
def logout():
    return redirect(url_for('auth.login'))