from flask import Blueprint, request, jsonify
from app.controllers import filme_controller

filmes_bp = Blueprint('filmes', __name__)

@filmes_bp.route('/filmes', methods=['POST'])
def criar_filme():
    data = request.get_json()
    resp, status = filme_controller.criar_filme(data)
    return jsonify(resp), status

@filmes_bp.route('/filmes', methods=['GET'])
def listar_filmes():
    return jsonify(filme_controller.listar_filmes())

@filmes_bp.route('/filmes/<int:codigo>', methods=['PUT'])
def atualizar_filme(codigo):
    data = request.get_json()
    resp = filme_controller.atualizar_filme(codigo, data)
    return jsonify(resp)

@filmes_bp.route('/filmes/<int:codigo>', methods=['DELETE'])
def deletar_filme(codigo):
    resp = filme_controller.deletar_filme(codigo)
    return jsonify(resp)
