from flask_mail import Message
from flask import render_template, current_app
from app_folder.extensions import mail
from app_folder.tasks import celery

@celery.task
def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    mail.send(msg)

