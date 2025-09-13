from flask import jsonify
from app.extensions import db
from app.models.aluguel import Aluguel
from app.models.cliente import Cliente
from app.models.filme import Filme
from datetime import datetime

def criar_aluguel(data):
    cpf_cliente = data.get("cliente_cpf")
    codigo_filme = data.get("codigo_filme")
    valor_diaria = data.get("valor_diaria")

    # Validar cliente
    cliente = Cliente.query.filter_by(cpf=cpf_cliente).first()
    if not cliente:
        return {"erro": f"Cliente com CPF {cpf_cliente} não encontrado"}, 404

    # Validar filme
    filme = Filme.query.filter_by(id=codigo_filme).first()
    if not filme:
        return {"erro": f"Filme com ID {codigo_filme} não encontrado"}, 404
    if not filme.disponivel:
        return {"erro": f"Filme '{filme.nome_filme}' não está disponível"}, 400

    # Evitar duplicidade de aluguel ativo
    aluguel_existente = Aluguel.query.filter_by(cliente_cpf=cpf_cliente, filme_id=codigo_filme, status=True).first()
    if aluguel_existente:
        return {"erro": "Este cliente já possui este filme alugado"}, 400

    # Criar aluguel
    aluguel = Aluguel(
        cliente_cpf=cpf_cliente,
        filme_id=codigo_filme,
        valor_diaria=valor_diaria,
        data_aluguel=datetime.now(),
        status=True
    )
    filme.disponivel = False
    db.session.add(aluguel)
    db.session.commit()

    return {"mensagem": "Aluguel criado com sucesso", "aluguel_id": aluguel.id}, 201


def listar_alugueis():
    alugueis = Aluguel.query.all()
    result = []
    for aluguel in alugueis:
        result.append({
            "id": aluguel.id,
            "cpf_cliente": aluguel.cliente_cpf,
            "codigo_filme": aluguel.filme_id,
            "data_aluguel": aluguel.data_aluguel.isoformat() if aluguel.data_aluguel else None,
            "data_devolucao": aluguel.data_devolucao.isoformat() if aluguel.data_devolucao else None,
            "valor": aluguel.valor,
            "status": aluguel.status
        })
    return jsonify(result)


def atualizar_aluguel(id, data):
    aluguel = Aluguel.query.get(id)
    if not aluguel:
        return {"erro": "Aluguel não encontrado"}, 404

    # Atualizar apenas campos permitidos
    for campo in ["valor_diaria", "data_aluguel", "data_devolucao", "status"]:
        if campo in data:
            setattr(aluguel, campo, data[campo])

    # Se devolver, calcular tempo e valor
    if data.get("status") is False and aluguel.status:  # devolução
        aluguel.data_devolucao = datetime.now()
        aluguel.tempo_aluguel = (aluguel.data_devolucao - aluguel.data_aluguel).days
        aluguel.valor = aluguel.tempo_aluguel * aluguel.valor_diaria
        # Liberar o filme
        filme = Filme.query.get(aluguel.filme_id)
        filme.disponivel = True

    db.session.commit()
    return {"mensagem": "Aluguel atualizado com sucesso"}


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
    return {"mensagem": "Aluguel deletado com sucesso"}


def listar_alugueis_por_cliente(cpf_cliente):
    alugueis = Aluguel.query.filter_by(cliente_cpf=cpf_cliente).all()
    if not alugueis:
        return {"erro": "Nenhum aluguel encontrado para este cliente"}, 404

    result = []
    for aluguel in alugueis:
        result.append({
            "id": aluguel.id,
            "codigo_filme": aluguel.filme_id,
            "data_aluguel": aluguel.data_aluguel.isoformat() if aluguel.data_aluguel else None,
            "data_devolucao": aluguel.data_devolucao.isoformat() if aluguel.data_devolucao else None,
            "valor": aluguel.valor,
            "status": aluguel.status
        })
    return jsonify(result)