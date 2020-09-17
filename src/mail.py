from flask import render_template
from flask_mail import Mail, Message

from app import app
from src.models import User

mail = Mail(app)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_magic_link(email):

    user = User.query.filter_by(email=email).first()

    send_email(
        "Аутентификация через email",
        sender=app.config["ADMINS"][0],
        recipients=[user.email],
        text_body=render_template("magic_link.txt", token=user.token),
        html_body=render_template("magic_link.html", token=user.token),
    )
