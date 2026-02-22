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
        return {"erro": f"Filme '{filme.titulo}' não está disponível"}, 400

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
    return [a.to_dict() for a in alugueis], 200


def atualizar_aluguel(id, data):
    aluguel = Aluguel.query.get(id)
    if not aluguel:
        return {"erro": "Aluguel não encontrado"}, 404
    
    status_original = aluguel.status

    for campo, valor in data.items():
        if campo not in ['status', 'data_devolucao']:
            setattr(aluguel, campo, valor)
    
    # if "data_devolucao" in data and data["data_devolucao"]:
    #     aluguel.data_devolucao = datetime.fromisoformat(data["data_devolucao"].replace("Z", "+00:00"))

    # status_enviado = data.get("status")
    # devolucao = False
    # if status_enviado in [False, 0, "0", "false", "False"] and status_original:
    #     devolucao = True

    if data.get("data_devolucao") and status_original:
        aluguel.status = False
        aluguel.data_devolucao = datetime.now()
        aluguel.tempo_aluguel = (aluguel.data_devolucao - aluguel.data_aluguel).days or 1
        aluguel.valor = aluguel.tempo_aluguel * aluguel.valor_diaria

        filme = Filme.query.get(aluguel.filme_id)
        filme.disponivel = True
    else:
        status_enviado = data.get("status")
        if status_enviado is not None:
            aluguel.status = bool(status_enviado)

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