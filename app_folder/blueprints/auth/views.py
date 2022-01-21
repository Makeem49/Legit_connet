from crypt import methods
from multiprocessing.dummy import current_process
from flask import request, render_template, g, redirect, url_for, flash
from app_folder.blueprints.auth import auth
from app_folder.blueprints.auth.forms import RegisterForm, LoginForm, ForgetPassword, ResetPasswordForm
from app_folder.blueprints.users.model import User
from app_folder.extensions import db
from app_folder.email import send_mail
import os 
from lib.safe_next_url import is_safe_url
from flask_login import login_user, login_required, logout_user, current_user
from lib.custom_token import serializer

@auth.before_request 
def get_current_blueprint():
    g.name = request.endpoint
    g.active = 'active'

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = db.session.query(User).filter_by(email=email).first()
        if user and user.verify_password(form.password.data):
            next_page = request.args.get('next')
            if login_user(user, remember=form.remember_me.data) and user.is_active():
                if next_page:
                    return redirect(is_safe_url(next_page))
                else:
                    flash('You have successfully logged in', 'success')
                    return redirect(url_for('user.profile'))
            else:
                flash("Your account has been deactivated, please contact the admin re-access your account.", 'info')
        elif user is None:
            flash('There is no user associated with this account, please register to access this page.', 'warning')
        else:
            flash("Incorrect credentials", 'warning')
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
            user = User(surname=surname, first_name=first_name, email=email, password=password, gender=gender, 
                                                        session_token=serializer().dumps([surname, password]))
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_mail.delay(email, 'Legit Connet Account Confirmation', 'mail/registration', name=user.first_name, token=token )
            flash('Your account has been register, you can now login to access your account', 'success')
            return redirect(url_for('auth.login'))
        else: 
            flash('There is an account associated with this email, kindly register with different email address.', 'info')
            return redirect(url_for('auth.register'))
    return render_template('register.html', form=form)

@auth.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('user.profile'))
    form = ForgetPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_password_rest_token()
            print(user)
            send_mail.delay(user.email, 'Legit Password Reset', 'mail/resetpassword', name=user.first_name, token=token)
            flash('A password reset link has been sent to your email address.', 'success')
            return redirect(url_for('auth.login'))
        else: 
            flash('There is not account associated with this email address, register to have access.', 'warning') 
            return redirect(url_for('auth.register'))
    return render_template('forget_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('page.profile'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        new_password = form.password.data
        user = User.confirm_password_reset_token(token, new_password)
        if user:
            flash('Password reset successfully.' , 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid or expired token.', 'warning')
    return render_template('password_reset.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have successfully logout", 'success')
    return redirect(url_for('page.home'))

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('user.profile'))
    if current_user.confirm_token(token):
        flash('You account has been confirmed', 'success')
    else: 
        flash("Invalid token or token expired", 'error')
    return redirect(url_for('user.profile'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[0:5] != 'auth.':  
        return redirect(url_for('auth.unconfirm'))
    
@auth.route('unconfirm')
def unconfirm():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('page.home'))
    return render_template('unconfirmed.html')


@auth.route('resend_confirmation')
@login_required
def resend_confirmation():
    if current_user.confirmed:
        return redirect(url_for('page.profile'))
    token = current_user.generate_confirmation_token()
    send_mail.delay(current_user.email, 'Account Confirmation', 'mail/registration', token=token)
    flash('Activation link sent.', 'success')
    return redirect(url_for('auth.unconfirm'))
