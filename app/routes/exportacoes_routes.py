from flask import Blueprint, jsonify, request, send_file

from app.controllers import exportacao_controller

exportacoes_bp = Blueprint('exportacoes_bp', __name__, url_prefix='/exportacoes')


@exportacoes_bp.route('', methods=['POST'])
def gerar_exportacao():
    data = request.get_json() or {}
    tipo = data.get('tipo')
    formato = data.get('formato')
    inicio = data.get('inicio')
    fim = data.get('fim')

    try:
        resultado = exportacao_controller.gerar_exportacao(tipo, formato, inicio, fim)
        registro = exportacao_controller.registrar_historico(
            tipo=resultado['tipo_relatorio'],
            formato=formato,
            inicio=resultado['inicio'],
            fim=resultado['fim'],
            total_registros=resultado['total_registros'],
            tamanho_bytes=resultado['tamanho_bytes'],
            status='sucesso'
        )
    except ValueError as exc:
        exportacao_controller.registrar_historico(
            tipo=tipo or 'desconhecido',
            formato=formato or 'csv',
            status='erro',
            mensagem=str(exc)
        )
        return jsonify({'erro': str(exc)}), 400
    except Exception as exc:
        exportacao_controller.registrar_historico(
            tipo=tipo or 'desconhecido',
            formato=formato or 'csv',
            status='erro',
            mensagem=str(exc)
        )
        return jsonify({'erro': 'Falha ao gerar relatório'}), 500

    response = send_file(
        resultado['buffer'],
        mimetype=resultado['mimetype'],
        as_attachment=True,
        download_name=resultado['filename']
    )
    response.headers['X-Historico-Id'] = str(registro.id)
    response.headers['X-Total-Registros'] = str(resultado['total_registros'])
    response.headers['X-Relatorio-Tipo'] = resultado['tipo_relatorio']
    return response


@exportacoes_bp.route('/historico', methods=['GET'])
def listar_historico():
    limite = request.args.get('limit', 20)
    registros = exportacao_controller.listar_historico(limite)
    return jsonify(registros)
