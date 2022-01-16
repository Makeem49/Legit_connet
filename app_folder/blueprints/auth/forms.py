from flask_wtf import  FlaskForm
from wtforms import StringField, PasswordField, RadioField, EmailField, SubmitField, BooleanField
from wtforms.validators import InputRequired, EqualTo, Email, ValidationError
from app_folder.blueprints.users.model import User

def custom_keywords():
    return {"aria-describedby":"inputGroupPrepend3 validationServerUsernameFeedback"}


class RegisterForm(FlaskForm):
    surname = StringField('Surname', [InputRequired()], render_kw=custom_keywords())
    name = StringField('First name', [InputRequired()], render_kw=custom_keywords())
    email = EmailField('Email', [InputRequired(), Email(message='Email is required')], render_kw=custom_keywords())
    password = PasswordField("password", [InputRequired()])
    confirm_password = PasswordField("Confirm pasword", [ InputRequired(), EqualTo('password', message='Password must match') ])
    gender = RadioField('Gender', choices=['male', 'female'])

    def validate_email(self, email):
        user = User.query.filter_by(email=email)
        if user: 
            raise ValidationError('There is a user with email account.')
    
    def validate_username(self, surname):
        user = User.query.filter_by(surname=surname)
        if user: 
            raise ValidationError('There is a user with email account.')


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