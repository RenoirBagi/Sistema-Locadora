import os
import pymysql
from app.extensions import db

def init_db(app):
    """
    Inicializa a base de dados MySQL com o app Flask e o SQLAlchemy.
    Cria o banco automaticamente se não existir.
    """
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', 'root')
    db_name = os.getenv('DB_NAME', 'sistema_locadora')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = int(os.getenv('DB_PORT', 3306))

    # Conexão bruta para criar o banco caso não exista
    conn = pymysql.connect(host=db_host, user=db_user, password=db_password, port=db_port)
    cursor = conn.cursor()
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {db_name} "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    )
    conn.commit()
    cursor.close()
    conn.close()

    # Configuração SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)