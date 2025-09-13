from flask import Blueprint, request, jsonify
from app.controllers import aluguel_controller

alugueis_bp = Blueprint('alugueis', __name__)

@alugueis_bp.route('/alugueis', methods=['POST'])
def criar_aluguel():
    data = request.get_json()
    resp, status = aluguel_controller.criar_aluguel(data)
    return jsonify(resp), status

@alugueis_bp.route('/alugueis', methods=['GET'])
def listar_alugueis():
    return jsonify(aluguel_controller.listar_alugueis())

@alugueis_bp.route('/alugueis/<int:id>', methods=['PUT'])
def atualizar_aluguel(id):
    data = request.get_json()
    resp = aluguel_controller.atualizar_aluguel(id, data)
    return jsonify(resp)

@alugueis_bp.route('/alugueis/<int:id>', methods=['DELETE'])
def deletar_aluguel(id):
    resp = aluguel_controller.deletar_aluguel(id)
    return jsonify(resp)