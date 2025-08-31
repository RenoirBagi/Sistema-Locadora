from Config import db
import Classes
from flask import request
from flask import jsonify

def init_routes(app):  
    @app.route('/home', methods=['GET'])
    def home():
        return jsonify({'mensagem': "Subiu eu acho"})

    @app.route('/alugar', methods=['POST'])
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
    
    

    

