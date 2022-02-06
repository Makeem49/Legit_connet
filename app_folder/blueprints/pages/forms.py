from flask_wtf import FlaskForm 
from wtforms import TextAreaField, SubmitField
from wtforms.validators import InputRequired


class PostForm(FlaskForm):
    content = TextAreaField('Content', [InputRequired()])
    submit = SubmitField('Post')