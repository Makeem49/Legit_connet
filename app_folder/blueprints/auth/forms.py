from flask_wtf import  FlaskForm
from wtforms import StringField, PasswordField, RadioField, EmailField, SubmitField, BooleanField, DateField
from wtforms.validators import InputRequired, EqualTo, Email, ValidationError, Optional
from app_folder.blueprints.users.model import User
from flask_login import current_user

def custom_keywords():
    return {"aria-describedby":"inputGroupPrepend3 validationServerUsernameFeedback"}


class RegisterForm(FlaskForm):
    surname = StringField('Surname', [InputRequired()], render_kw=custom_keywords())
    name = StringField('First name', [InputRequired()], render_kw=custom_keywords())
    email = EmailField('Email', [InputRequired(), Email(message='Email is required')], render_kw=custom_keywords())
    password = PasswordField("password", [InputRequired()])
    confirm_password = PasswordField("Confirm pasword", [ InputRequired(), EqualTo('password', message='Password must match') ])
    gender = RadioField('Gender', [InputRequired()] ,choices=['male', 'female'])
    username = StringField('Username', [InputRequired()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user: 
            raise ValidationError('There is a user with email account.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('There is a user with this username.')

class LoginForm(FlaskForm):
    email = EmailField('Email', [InputRequired(), Email(message='Email is required')])
    password = PasswordField("Password", [InputRequired()])
    remember_me = BooleanField('Rememeber me')
    submit = SubmitField("Sign in")


class ForgetPassword(FlaskForm):
    email = EmailField('Email', [InputRequired(), Email(message='Email is required')])
    submit = SubmitField('Request password reset link')

class ResetPasswordForm(FlaskForm):
    password = PasswordField("password", [InputRequired()])
    confirm_password = PasswordField("Confirm pasword", [ InputRequired(), EqualTo('password', message='Password must match') ])


class UpdateEmailAddress(FlaskForm):
    new_email = EmailField('New email', [InputRequired()])
    confirm_email = EmailField('Confirm email', [InputRequired(), EqualTo('new_email', message='Password must match')])
    password = PasswordField('Password', [InputRequired()])

    def validate_password(self, password):
        user = User.query.filter_by(email=current_user.email).first()
        if not user.verify_password(password.data):
            raise ValidationError(f'Password not correct, we need to verify {current_user.username} authorise this update')
            