from email import message
from flask import Flask
from flask_wtf import FlaskForm 
from wtforms import (SelectField, StringField, EmailField, RadioField, SelectField, 
                                BooleanField, DateTimeField)
from wtforms.validators import InputRequired, Email, Optional, ValidationError

from app_folder.blueprints.users.model import Role, User


class AdminEditUserForm(FlaskForm):
    # User editform form
    email = EmailField('Email', [InputRequired(), Email(message='Email cannot be empty.')])
    username = StringField('Username', [InputRequired()])
    first_name = StringField('First name', [InputRequired()])
    last_name = StringField('Last name', [InputRequired()])
    gender = RadioField('Gender', [InputRequired()], choices=['male', 'female'], )
    confirmed = StringField('Confirmed', [Optional()])
    active = BooleanField("Active", [Optional])
    member_since = DateTimeField("Member since", [InputRequired()])
    job_title = StringField('Job title', [Optional()])
    education = StringField("Education", [Optional()])
    course = StringField("Education", [Optional()])
    role = SelectField('Role', coarse=int)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.role.choices = [(self.role.id , self.role.name) for role in Role.query.all().order_by(Role.name)]

        self.user = user 


    def validate_email(self, email):
        if email.data != self.user.email and User.query.filter_by(email=email.data).first():
            raise ValidationError("There is a user associated with this email")

    def validate_username(self, username):
        if username.data != self.user.username and User.query.filter_by(username = username.data).first():
            raise ValidationError("There is a user with this username.")

    
