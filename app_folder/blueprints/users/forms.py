from flask_wtf import  FlaskForm
from sqlalchemy.orm.mapper import validates
from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    surname = StringField('Surname', [DataRequired()])
    name = StringField('First name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField("password", [DataRequired()])
    # confirm_password = PasswordField('Confirm Password', validators=[Required(), EqualTo('password', message='Passwords must match')])
    confirm_password = PasswordField("Confirm pasword", [ DataRequired(), EqualTo('password', message='Password must match') ])
    gender = RadioField('Gender', choices=['male', 'female'])