import sys
from flask_sqlalchemy import SQLAlchemy
import os
import pymysql

db = SQLAlchemy()

def init_db(app):
    """
    Inicializa a base de dados com o app Flask e o SQLAlchemy.
    """
    db_user = 'root'
    db_password = 'root'
    db_name = 'locadora'
    db_host = 'localhost'
    db_port = 3306

    conn = pymysql.connect(host=db_host, user=db_user, password=db_password, port=db_port)
    cursor = conn.cursor()
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {db_name} "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    )
    conn.commit()
    cursor.close()
    conn.close()

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@localhost/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

