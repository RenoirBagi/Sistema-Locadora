from Config import db
import Classes
from flask import request
from flask import jsonify

def init_routes(app):  
    @app.route('/home', methods=['GET'])
    def home():
        return jsonify({'mensagem': "Subiu eu acho"})
    
    @app.route('/api/alugar/buscar', methods=['GET'])
    def buscar_filmes():
        data = request.json
        nome_parcial = data.get('nome')
        session = db.session
        filmes = Classes.Filme.buscar_filmes(session, nome_parcial)
        resultado = [
            {"id": filme.id, "nome": filme.nome_filme, "disponivel": filme.disponivel} 
            for filme in filmes
        ]
        return jsonify(resultado)


    @app.route('/api/alugar', methods=['POST'])
    def alugar_filme():
        data = request.json
        cliente_cpf = data.get('cliente_cpf')
        filme_id = data.get('filme_id')
        valor_diaria = data.get('valor_diaria')
        try:
            mensagem = Classes.Aluguel.fazer_aluguel(db.session, cliente_cpf, filme_id, valor_diaria)
            return jsonify({'mensagem':mensagem}), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 400
    
    

    

