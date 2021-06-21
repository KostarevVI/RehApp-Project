import os
import babel
import configparser
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
app = Flask(__name__)
config = configparser.ConfigParser()
config.read('config.ini')

app.config['SECRET_KEY'] = config.get("Settings", "app_secret_key", fallback="No such thing as app_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = config.get("Settings", "database_url", fallback="No such thing as database_url")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = config.get("Settings", "email_user", fallback="No such thing as email_user")
app.config['MAIL_PASSWORD'] = config.get("Settings", "email_pass", fallback="No such thing as email_pass")
app.config['RECAPTCHA_PRIVATE_KEY'] = config.get("Settings", "captcha_private",
                                                 fallback="No such thing as captcha_private")
app.config['RECAPTCHA_PUBLIC_KEY'] = config.get("Settings", "captcha_public",
                                                fallback="No such thing as captcha_public")

app.config['TESTING'] = False
mail = Mail(app)


# export EMAIL_USER="rehapp.project@gmail.com"
# export EMAIL_PASS="mvstyEz0pklICbR&z!9D"
# export APP_SECRET_KEY=";ofija839P(#*J#@P89JFP#(*JppPJI@PE* pJ p8J QP(@*Jp9e28jF))DA.?????/dS?"
# export DATABASE_URL="postgresql+psycopg2://postgres:6559@localhost/rehapp_database"



def create_app():
    global db
    global app

    db = SQLAlchemy(app, session_options={"expire_on_commit": False})

    from .auth import auth
    from .rehapp import rehapp
    # from .play_screen import play_screen
    #
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(rehapp, url_prefix='/')
    # app.register_blueprint(play_screen, url_prefix='/')

    from .models import Therapist

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Therapist.query.get(int(id))

    return app
