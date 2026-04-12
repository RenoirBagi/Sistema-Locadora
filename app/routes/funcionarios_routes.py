from flask import Blueprint
from app.controllers import funcionario_controller

funcionarios_bp = Blueprint("funcionarios", __name__, url_prefix="/funcionarios")

@funcionarios_bp.route("/", methods=["GET"])
def listar_funcionarios():
    return funcionario_controller.listar_funcionarios()

@funcionarios_bp.route("/", methods=["POST"])
def criar_funcionario():
    return funcionario_controller.criar_funcionario()

@funcionarios_bp.route("/<string:cpf>", methods=["PUT", "PATCH"])
def editar_funcionario(cpf):
    return funcionario_controller.editar_funcionario(cpf)

@funcionarios_bp.route("/<string:cpf>", methods=["DELETE"])
def remover_funcionario(cpf):
    return funcionario_controller.remover_funcionario(cpf)

