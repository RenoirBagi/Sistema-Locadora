from .clientes_routes import clientes_bp
from .filmes_routes import filmes_bp
from .alugueis_routes import alugueis_bp
from .dashboard_routes import dashboard_bp
from .exportacoes_routes import exportacoes_bp

def register_routes(app):
    app.register_blueprint(clientes_bp)
    app.register_blueprint(filmes_bp)
    app.register_blueprint(alugueis_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(exportacoes_bp)