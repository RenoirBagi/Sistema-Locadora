import os
from urllib.parse import quote_plus
from app.extensions import db

def init_db(app):
    """
    Inicializa a base de dados PostgreSQL (Supabase) com o app Flask e o SQLAlchemy.
    """
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'postgres')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')

    # Escapa caracteres especiais na senha e usuário para evitar erros de URL/Unicode
    safe_user = quote_plus(db_user)
    safe_password = quote_plus(db_password)

    # Configuração SQLAlchemy para PostgreSQL
    # Adicionamos sslmode=require pois o Pooler do Supabase exige conexão segura
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'postgresql://{safe_user}:{safe_password}@{db_host}:{db_port}/{db_name}?sslmode=require'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
