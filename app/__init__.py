from flask import Flask
from app.extensions import db
from app.config_db import init_db
from app.routes import register_routes

def create_app():
    """
    Função que cria e configura a aplicação Flask.
    """
    app = Flask(__name__)

    init_db(app)

    register_routes(app)

    with app.app_context():
        db.create_all()

    return app