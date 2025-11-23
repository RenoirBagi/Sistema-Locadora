from flask import Flask
from flask_cors import CORS
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

    CORS(app)

    with app.app_context():
        from app.models import aluguel  # noqa: F401
        from app.models import cliente  # noqa: F401
        from app.models import filme  # noqa: F401
        from app.models import historico_exportacao  # noqa: F401
        db.create_all()

    return app