from flask import request, jsonify
from app.extensions import db
from app.models.funcionario import Funcionario

def listar_funcionarios():
    try:
        funcionarios = Funcionario.query.all()
        return jsonify([f.to_dict() for f in funcionarios]), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def criar_funcionario():
    try:
        dados = request.get_json()
        required = ["cpf", "nome", "cargo", "contato", "endereco"]
        if not dados or not all(k in dados for k in required):
            return jsonify({"erro": "Dados incompletos"}), 400
        
        novo_funcionario = Funcionario(
            cpf=dados["cpf"],
            nome=dados["nome"],
            cargo=dados["cargo"],
            contato=dados["contato"],
            endereco=dados["endereco"]
        )
        db.session.add(novo_funcionario)
        db.session.commit()
        
        return jsonify(novo_funcionario.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500

def editar_funcionario(cpf):
    try:
        funcionario = Funcionario.query.get(cpf)
        if not funcionario:
            return jsonify({"erro": "Funcionário não encontrado"}), 404
            
        dados = request.get_json()
        if "nome" in dados:
            funcionario.nome = dados["nome"]
        if "cargo" in dados:
            funcionario.cargo = dados["cargo"]
        if "contato" in dados:
            funcionario.contato = dados["contato"]
        if "endereco" in dados:
            funcionario.endereco = dados["endereco"]
            
        db.session.commit()

        return jsonify(funcionario.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500

def remover_funcionario(cpf):
    try:
        funcionario = Funcionario.query.get(cpf)
        if not funcionario:
            return jsonify({"erro": "Funcionário não encontrado"}), 404
            
        db.session.delete(funcionario)
        db.session.commit()
        return jsonify({"mensagem": "Funcionário removido com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500

