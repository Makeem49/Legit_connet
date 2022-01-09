from flask_wtf import  FlaskForm
from sqlalchemy.orm.mapper import validates
from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email


class RegisterForm(FlaskForm):
    surname = StringField('Surname', [DataRequired()])
    name = StringField('First name', [DataRequired()])
    email = EmailField('Email', [DataRequired(), Email(message='Email is required')])
    password = PasswordField("password", [DataRequired()])
    confirm_password = PasswordField("Confirm pasword", [ DataRequired(), EqualTo('password', message='Password must match') ])
    gender = RadioField('Gender', choices=['male', 'female'])


class LoginForm(FlaskForm):
    email = EmailField('Email', [DataRequired(), Email(message='Email is required')])
    password = PasswordField("Password", [DataRequired()])
    remember_me = BooleanField('Rememeber me')
    submit = SubmitField("Sign in")


class ForgetPassword(FlaskForm):
    email = EmailField('Email', [DataRequired(), Email(message='Email is required')])
    submit = SubmitField('Request password reset link')

class ResetPasswordForm(FlaskForm):
    password = PasswordField("password", [DataRequired()])
    confirm_password = PasswordField("Confirm pasword", [ DataRequired(), EqualTo('password', message='Password must match') ])