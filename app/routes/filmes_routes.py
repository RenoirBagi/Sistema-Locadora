from flask import Blueprint, request, jsonify
from app.controllers import filme_controller

filmes_bp = Blueprint('filmes_bp', __name__, url_prefix='/filmes')

@filmes_bp.route('/', methods=['POST'])
def criar_filme():
    data = request.get_json()
    resp, status = filme_controller.criar_filme(data)
    return jsonify(resp), status

@filmes_bp.route('/', methods=['GET'])
def listar_filmes():
    busca = request.args.get('busca', type=str)
    resp, status = filme_controller.listar_filmes(busca)
    return jsonify(resp), status

@filmes_bp.route('/<int:id>', methods=['PUT'])
def atualizar_filme(id):
    data = request.get_json()
    resp, status = filme_controller.atualizar_filme(id, data)
    return jsonify(resp), status

@filmes_bp.route('/<int:id>', methods=['DELETE'])
def deletar_filme(id):
    resp, status = filme_controller.deletar_filme(id)
    return jsonify(resp), status
