from flask import request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
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
        required = ["cpf", "nome", "cargo", "contato", "endereco", "email", "senha"]
        if not dados or not all(k in dados for k in required):
            return jsonify({"erro": "Dados incompletos. Todos os campos são obrigatórios."}), 400
        
        # Validação de duplicidade
        if Funcionario.query.filter_by(cpf=dados["cpf"]).first():
            return jsonify({"erro": "CPF já cadastrado"}), 400
        if Funcionario.query.filter_by(email=dados["email"]).first():
            return jsonify({"erro": "E-mail já cadastrado"}), 400
        
        # Criptografa a senha usando o Werkzeug scrypt (padrão do Flask)
        senha_hash = generate_password_hash(dados["senha"])
        
        novo_funcionario = Funcionario(
            cpf=dados["cpf"],
            nome=dados["nome"],
            cargo=dados["cargo"],
            contato=dados["contato"],
            endereco=dados["endereco"],
            email=dados["email"],
            senha_hash=senha_hash,
            status="ativo"  # Todo funcionário recém-criado começa ativo
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
        if not dados:
            return jsonify({"erro": "Nenhum dado fornecido para atualização"}), 400

        # Atualizações condicionais
        if "nome" in dados:
            funcionario.nome = dados["nome"]
        if "cargo" in dados:
            funcionario.cargo = dados["cargo"]
        if "contato" in dados:
            funcionario.contato = dados["contato"]
        if "endereco" in dados:
            funcionario.endereco = dados["endereco"]
        
        # Gestão de novos campos de credenciais e status
        if "email" in dados:
            existente = Funcionario.query.filter_by(email=dados["email"]).first()
            if existente and existente.cpf != cpf:
                return jsonify({"erro": "E-mail já está em uso por outro funcionário"}), 400
            funcionario.email = dados["email"]
            
        if "senha" in dados and dados["senha"].strip():
            funcionario.senha_hash = generate_password_hash(dados["senha"])
            
        if "status" in dados:
            if dados["status"] not in ["ativo", "inativo"]:
                return jsonify({"erro": "Status inválido. Use 'ativo' ou 'inativo'."}), 400
            funcionario.status = dados["status"]
            
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

def login_funcionario():
    try:
        dados = request.get_json()
        if not dados or "email" not in dados or "senha" not in dados:
            return jsonify({"erro": "E-mail e senha são obrigatórios."}), 400
            
        email = dados["email"]
        senha = dados["senha"]
        
        funcionario = Funcionario.query.filter_by(email=email).first()
        
        # Tratamento seguro de credenciais com mensagem de erro genérica
        if not funcionario:
            return jsonify({"erro": "E-mail ou senha incorretos"}), 401
            
        if not check_password_hash(funcionario.senha_hash, senha):
            return jsonify({"erro": "E-mail ou senha incorretos"}), 401
            
        # Regra de negócio: apenas funcionários ativos podem logar
        if funcionario.status != "ativo":
            return jsonify({"erro": "Cadastro inativo. Entre em contato com o administrador."}), 403
            
        # Gera o token de acesso contendo o CPF como a identidade do JWT
        token = create_access_token(identity=funcionario.cpf)
        
        return jsonify({
            "token": token,
            "funcionario": funcionario.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

