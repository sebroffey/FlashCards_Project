from flask import Flask
from data import DB
from services import data_service
from web_api import auth, card, user


def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "secretkey"
    app.config["SESSION_PERMANENT"] = False



    app.register_blueprint(DB)
    app.register_blueprint(data_service)
    app.register_blueprint(auth)
    app.register_blueprint(card)
    app.register_blueprint(user)

    return app










