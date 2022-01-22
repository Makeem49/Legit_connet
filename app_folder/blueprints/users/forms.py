from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, StringField, DateField, TextAreaField
from wtforms.validators import ValidationError, Optional, InputRequired
from .model import User
from flask_login import current_user

def custom_keywords():
    return {"cols":10,"rows":20}

class UpdateCredentials(FlaskForm):
    surname = StringField('Surname', [Optional()])
    name = StringField('First name', [Optional()])
    password = PasswordField('Password', [InputRequired()])
    email = EmailField("Email", [Optional()])
    course = StringField('Course', [Optional()])
    education = StringField('Education', [Optional()])
    about_me = TextAreaField('About me', [Optional()])
    date_of_birth = DateField('Date of birth', [Optional()])   
    username = StringField("Username", [Optional()])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f'{username.data} is not available, choose another username.')

    def validate_email(self, email):
        user = User.query.filter_by(username=email.data).first()
        if user:
            raise ValidationError(f'{self.username.data} is not available, choose another username.')

    def validate_password(self, password):
        user = User.query.filter_by(email=current_user.email).first()
        if not user.verify_password(password.data):
            raise ValidationError('Incorrect pasword, we need to verify your account before updating it.')
    