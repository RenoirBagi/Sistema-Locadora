from app.extensions import db
from app.models.filme import Filme

def criar_filme(data):
    filme = Filme(**data)
    db.session.add(filme)
    db.session.commit()
    return {"mensagem": "Filme criado com sucesso", "id": filme.id}, 201

def listar_filmes(busca=None):
    query = Filme.query
    if busca:
        query = query.filter(Filme.titulo.ilike(f"%{busca}%"))
    filmes = query.all()
    return [f.to_dict() for f in filmes], 200

def atualizar_filme(id, data):
    filme = Filme.query.get(id)
    if not filme:
        return {"erro": "Filme não encontrado"}, 404
    for campo, valor in data.items():
        setattr(filme, campo, valor)
    db.session.commit()
    return {"mensagem": "Filme atualizado com sucesso"}, 200

def deletar_filme(id):
    filme = Filme.query.get(id)
    if not filme:
        return {"erro": "Filme não encontrado"}, 404
    db.session.delete(filme)
    db.session.commit()
    return {"mensagem": "Filme deletado com sucesso"}, 200