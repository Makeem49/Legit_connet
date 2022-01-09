from flask import request, render_template, g, redirect, url_for, flash
from app_folder.blueprints.auth import auth
from app_folder.blueprints.auth.forms import RegisterForm, LoginForm, ForgetPassword, ResetPasswordForm
from app_folder.blueprints.users.model import User
from app_folder.extensions import db



@auth.before_request 
def get_current_blueprint():
    g.name = request.endpoint
    g.active = 'active'

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print('Before validate')
    if form.validate_on_submit():
        print('validating')
        email = form.email.data
        user = db.session.query(User).filter_by(email=email).first()
        if user:
            if user.password == form.password.data:
                flash('You have successfully logged in', 'success')
                return redirect(url_for('user.profile'))
            else :
                flash('Incorrect password or email', 'warning')
                return redirect(url_for('auth.login'))
        else:
            flash('User not found, register to create an account', 'info')
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user is None:
            surname = form.surname.data
            first_name = form.name.data
            email = form.email.data
            password = form.password.data
            gender = form.gender.data
            user = User(surname=surname, first_name=first_name, email=email, password=password, gender=gender)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been register, you can now login to access your account', 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = ForgetPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('A password reset link has been sent to your email address', 'success')
            return redirect(url_for('auth.resetpassword'))
        else: 
            flash('There is not account associated with this email address, register to have access.', 'warning') 
            return redirect(url_for('auth.register'))       
    return render_template('forget_password.html', form=form)


@auth.route('/resetpassword', methods=['GET', 'POST'])
def resetpassword():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email='adminaccount@gmail.com')
        if user:
            user.password = form.password.data
            flash('Password reset successfully', 'success')
            return redirect(url_for('user.profile'))
    return render_template('resetpassword.html', form=form)


@auth.route('/logout')
def logout():
    return redirect(url_for('auth.login'))