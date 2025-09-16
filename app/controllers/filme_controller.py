from app.extensions import db
from app.models.filme import Filme

def criar_filme(data):
    filme = Filme(**data)
    db.session.add(filme)
    db.session.commit()
    return {"mensagem": "Filme criado com sucesso", "id": filme.id}, 201

def listar_filmes():
    filmes = Filme.query.all()
    result = []
    for filme in filmes:
        result.append({
            "id": filme.id,
            "titulo": filme.titulo,
            "genero": filme.genero,
            "ano": filme.ano,
            "preco": filme.preco,
            "disponivel": filme.disponivel
        })
    return result

def atualizar_filme(id, data):
    filme = Filme.query.get(id)
    if not filme:
        return {"erro": "Filme não encontrado"}, 404
    for campo, valor in data.items():
        setattr(filme, campo, valor)
    db.session.commit()
    return {"mensagem": "Filme atualizado com sucesso"}

def deletar_filme(id):
    filme = Filme.query.get(id)
    if not filme:
        return {"erro": "Filme não encontrado"}, 404
    db.session.delete(filme)
    db.session.commit()
    return {"mensagem": "Filme deletado com sucesso"}