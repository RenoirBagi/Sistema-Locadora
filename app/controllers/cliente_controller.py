from app.extensions import db
from app.models.cliente import Cliente

def criar_cliente(data):
    if Cliente.query.filter_by(cpf=data['cpf']).first():
        return {"erro": "CPF já cadastrado"}, 400

    cliente = Cliente(**data)
    db.session.add(cliente)
    db.session.commit()
    return {"mensagem": "Cliente criado com sucesso", "cpf": cliente.cpf}, 201

def listar_clientes():
    clientes = Cliente.query.all()
    result = []
    for cliente in clientes:
        result.append({
            "cpf": cliente.cpf,
            "nome": cliente.nome,
            "idade": cliente.idade,
            "contato": cliente.contato,
            "endereco": cliente.endereco
        })
    return result

def atualizar_cliente(cpf, data):
    cliente = Cliente.query.get(cpf)
    if not cliente:
        return {"erro": "Cliente não encontrado"}, 404
    for campo, valor in data.items():
        setattr(cliente, campo, valor)
    db.session.commit()
    return {"mensagem": "Cliente atualizado com sucesso"}

def deletar_cliente(cpf):
    cliente = Cliente.query.get(cpf)
    if not cliente:
        return {"erro": "Cliente não encontrado"}, 404
    db.session.delete(cliente)
    db.session.commit()
    return {"mensagem": "Cliente deletado com sucesso"}