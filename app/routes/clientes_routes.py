from flask import Blueprint, request, jsonify
from app.controllers.cliente_controller import criar_cliente, listar_clientes, atualizar_cliente, deletar_cliente

clientes_bp = Blueprint('clientes_bp', __name__, url_prefix='/clientes')

@clientes_bp.route('/', methods=['POST'])
def criar():
    data = request.get_json()
    resp, status = criar_cliente(data)
    return jsonify(resp), status

@clientes_bp.route('/', methods=['GET'])
def listar():
    resp, status = listar_clientes()
    return jsonify(resp), status

@clientes_bp.route('/<cpf>', methods=['PUT'])
def atualizar(cpf):
    data = request.get_json()
    resp, status = atualizar_cliente(cpf, data)
    return jsonify(resp), status

@clientes_bp.route('/<cpf>', methods=['DELETE'])
def deletar(cpf):
    resp, status = deletar_cliente(cpf)
    return jsonify(resp), status