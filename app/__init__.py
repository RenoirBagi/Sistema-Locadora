from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.extensions import db
from app.config_db import init_db
from app.routes import register_routes

load_dotenv()

def create_app():
    """
    Função que cria e configura a aplicação Flask.
    """
    app = Flask(__name__)

    init_db(app)

    CORS(app)

    register_routes(app)

    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    return app