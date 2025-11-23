# from flask import Flask
# from Config import init_db, db
# from routes import init_routes
# from Classes import Cliente, Filme, Aluguel

# def create_app():
#     """
#     Função que cria e configura a aplicação Flask.
#     """
#     app = Flask(__name__)

#     init_db(app)

#     init_routes(app)

#     return app

# app = create_app()

# with app.app_context():
#     db.create_all()

# if __name__ == '__main__':
#     app.run(debug=True)


from app import create_app

flask_app = create_app()

if __name__ == '__main__':
    flask_app.run(debug=True)