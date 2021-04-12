from flask import Flask
from config import Config
from extensions import db

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    register_blueprints(app)
    
    return app



def register_blueprints(app):
    
    from web_api.auth import auth_routes
    from web_api.card import card_routes
    from web_api.user import user_routes

    app.register_blueprint(auth_routes)
    app.register_blueprint(card_routes)
    app.register_blueprint(user_routes)





