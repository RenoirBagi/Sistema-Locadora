from flask import Blueprint, jsonify, request

from app.controllers import dashboard_controller


dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/resumo', methods=['GET'])
def obter_resumo():
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')
    dados = dashboard_controller.obter_resumo(inicio, fim)
    return jsonify(dados)


@dashboard_bp.route('/series', methods=['GET'])
def obter_series():
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')
    dados = dashboard_controller.obter_series(inicio, fim)
    return jsonify(dados)


@dashboard_bp.route('/top-generos', methods=['GET'])
def obter_top_generos():
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')
    limite = request.args.get('limit', 5)
    dados = dashboard_controller.obter_top_generos(inicio, fim, limite)
    return jsonify(dados)


@dashboard_bp.route('/status', methods=['GET'])
def obter_status():
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')
    dados = dashboard_controller.obter_status(inicio, fim)
    return jsonify(dados)


@dashboard_bp.route('/top-filmes', methods=['GET'])
def obter_top_filmes():
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')
    limite = request.args.get('limit', 5)
    dados = dashboard_controller.obter_top_filmes(inicio, fim, limite)
    return jsonify(dados)
