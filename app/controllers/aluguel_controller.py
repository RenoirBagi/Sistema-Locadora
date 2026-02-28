from flask import jsonify
from app.extensions import db
from app.models.aluguel import Aluguel
from app.models.cliente import Cliente
from app.models.filme import Filme
from datetime import datetime

def criar_aluguel(data):
    cpf_cliente = data.get("cliente_cpf")
    codigo_filme = data.get("codigo_filme")
    data_devolucao_str = data.get("data_devolucao_prevista")

    if not data_devolucao_str:
        return {"erro": "A data de devolução prevista é obrigatória"}, 400

    try:
        data_devolucao_prevista = datetime.fromisoformat(data_devolucao_str)
    except (ValueError, TypeError):
        return {"erro": "Data de devolução inválida. Use o formato AAAA-MM-DD"}, 400

    data_aluguel = datetime.now()

    if data_devolucao_prevista.date() <= data_aluguel.date():
        return {"erro": "A data de devolução deve ser posterior à data atual"}, 400

    # Validar cliente
    cliente = Cliente.query.filter_by(cpf=cpf_cliente).first()
    if not cliente:
        return {"erro": f"Cliente com CPF {cpf_cliente} não encontrado"}, 404

    # Validar filme
    filme = Filme.query.filter_by(id=codigo_filme).first()
    if not filme:
        return {"erro": f"Filme com ID {codigo_filme} não encontrado"}, 404
    if not filme.disponivel:
        return {"erro": f"Filme '{filme.titulo}' não está disponível"}, 400

    # Evitar duplicidade de aluguel ativo
    aluguel_existente = Aluguel.query.filter_by(cliente_cpf=cpf_cliente, filme_id=codigo_filme, status=True).first()
    if aluguel_existente:
        return {"erro": "Este cliente já possui este filme alugado"}, 400

    # Calcular período e valor
    tempo_aluguel = (data_devolucao_prevista.date() - data_aluguel.date()).days or 1
    valor_diaria = filme.preco
    valor_total = tempo_aluguel * valor_diaria

    # Criar aluguel
    aluguel = Aluguel(
        cliente_cpf=cpf_cliente,
        filme_id=codigo_filme,
        valor_diaria=valor_diaria,
        data_aluguel=data_aluguel,
        data_devolucao_prevista=data_devolucao_prevista,
        tempo_aluguel=tempo_aluguel,
        valor=valor_total,
        status=True
    )
    filme.disponivel = False
    db.session.add(aluguel)
    db.session.commit()

    return {"mensagem": "Aluguel criado com sucesso", "aluguel_id": aluguel.id}, 201


def listar_alugueis():
    alugueis = Aluguel.query.all()
    return [a.to_dict() for a in alugueis], 200


def atualizar_aluguel(id, data):
    aluguel = Aluguel.query.get(id)
    if not aluguel:
        return {"erro": "Aluguel não encontrado"}, 404

    if not aluguel.status:
        return {"erro": "Este aluguel já foi finalizado"}, 400

    if data.get("devolver"):
        aluguel.status = False
        aluguel.data_devolucao = datetime.now()

        filme = Filme.query.get(aluguel.filme_id)
        if filme:
            filme.disponivel = True

    db.session.commit()
    return {"mensagem": "Aluguel atualizado com sucesso"}, 200


def deletar_aluguel(id):
    aluguel = Aluguel.query.get(id)
    if not aluguel:
        return {"erro": "Aluguel não encontrado"}, 404

    # Liberar filme caso ainda esteja alugado
    if aluguel.status:
        filme = Filme.query.get(aluguel.filme_id)
        filme.disponivel = True

    db.session.delete(aluguel)
    db.session.commit()
    return {"mensagem": "Aluguel deletado com sucesso"}, 200


def listar_alugueis_por_cliente(cpf_cliente):
    alugueis = Aluguel.query.filter_by(cliente_cpf=cpf_cliente).all()
    if not alugueis:
        return {"erro": "Nenhum aluguel encontrado para este cliente"}, 404

    return [a.to_dict() for a in alugueis], 200