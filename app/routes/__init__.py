from .clientes_routes import clientes_bp
from .filmes_routes import filmes_bp
from .alugueis_routes import alugueis_bp

def register_routes(app):
    app.register_blueprint(clientes_bp)
    app.register_blueprint(filmes_bp)
    app.register_blueprint(alugueis_bp)