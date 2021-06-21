from threading import Thread
from .__name__ import app, mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(msg):

    Thread(target=send_async_email, args=(app, msg)).start()
