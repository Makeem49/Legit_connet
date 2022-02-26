from flask_wtf import FlaskForm 
from wtforms import TextAreaField, SubmitField, SelectField
from wtforms.validators import InputRequired


class PostForm(FlaskForm):
    content = TextAreaField('Content', [InputRequired()])
    hash_tag = SelectField('Category', choices=[('all', "All"),
        ("world", "World"),
        ("u.s", "U.S"),
        ("technology", "Technology"),
        ("design", "Design"),
        ("culture", "Culture"),
        ("business", "Business"),
        ("politics", "Politics"),
        ("opinion", "Opinion"),
        ("science", "Science"),
        ("style", "Style"),
        ("travel", "Travel")
        ])
    submit = SubmitField('Post')