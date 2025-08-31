from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from Error import *
from Config import *
from datetime import datetime
from Locadora import main

class Cliente(db.Model):
    __tablename__ = 'clientes'

    cpf = db.Column(db.String(11), primary_key=True)  # CPF como chave primária
    nome = db.Column(db.String(60), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    contato = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)

    alugueis = relationship("Aluguel", back_populates="cliente")

    def cadastrar_cliente(cpf, nome, idade, contato, endereco):
        if idade<18:
            raise MenorDeIdadeError("\nOps, parece que o apressadinho não tem 18 anos!")
        
        cliente_existente = db.session.query(Cliente).filter_by(cpf = cpf).first()
        if cliente_existente:
            limpar_tela()
            raise ElementoExistenteError(f"\nErro: O CPF '{cpf}' já está cadastrado para outro cliente.")

        novo_cliente = Cliente(cpf = cpf, nome = nome, idade = idade, contato = contato, endereco = endereco)
        db.session.add(novo_cliente)
        print(f"\nCliente '{nome}' criado com sucesso!")
        db.session.commit()
        
        menu_saida()
    
    def consultar_cliente(session, cpf):
        cliente = session.query(Cliente).filter_by(cpf=cpf).first()
        if not cliente:
            raise ElementoNaoEncontradoError(f"\nErro: O cliente não foi encontrado.")

        print(f"\nCPF: {cliente.cpf}")
        print(f"Nome: {cliente.nome}")
        print(f"Idade: {cliente.idade}")
        print(f"Contato: {cliente.contato}")
        print(f"Endereço: {cliente.endereco}")

        menu_saida()

    def listar_clientes(session):
    # Ordena a lista de clientes pelo atributo 'nome'
        clientes = session.query(Cliente).order_by(Cliente.nome).all()
        if clientes:
            print("\nClientes:")
            for cliente in clientes:
                print(f"Nome: {cliente.nome} | CPF: {cliente.cpf} | Idade: {cliente.idade} | Contato: {cliente.contato} | Endereço: {cliente.endereco}")
        else:
            raise ElementoNaoEncontradoError("\nNenhum cliente encontrado.")

        menu_saida()

    def alterar_cliente(session, cpf):
        cliente = session.query(Cliente).filter_by(cpf=cpf).first()
        if not cliente:
            raise ElementoNaoEncontradoError(f"\nErro: O cliente '{cpf}' não foi encontrado.")

        print(f"\nCPF: {cliente.cpf}")
        print(f"Nome: {cliente.nome}")
        print(f"Idade: {cliente.idade}")
        print(f"Contato: {cliente.contato}")
        print(f"Endereço: {cliente.endereco}")

        print("\nescolaha uma opção:")
        print("========================================")
        print("1 - Editar nome")
        print("2 - Editar idade")
        print("3 - Editar contato")
        print("4 - Editar endereço")
        print("5 - Editar todos os dados")
        print("0 - Sair")
        print("========================================")

        opcao = obter_input("Escolha uma opção: ", int)

        if opcao == 1:
            novo_nome = obter_input("Digite o novo nome: ")
            cliente.nome = novo_nome
            session.commit()
            print(f"\nNome atualizado para: {novo_nome}")
        elif opcao == 2:
            novo_idade = obter_input("Digite a nova idade: ", int) 
            cliente.idade = novo_idade
            session.commit()
            print(f"\nIdade atualizada para: {novo_idade}")
        elif opcao == 3:
            novo_contato = obter_input("Digite o novo contato: ")
            cliente.contato = novo_contato
            session.commit()
            print(f"\nContato atualizado para: {novo_contato}")
        elif opcao == 4:
            novo_endereco = obter_input("Digite o novo endereço: ")
            cliente.endereco = novo_endereco
            session.commit()
            print(f"\nEndereço atualizado para: {novo_endereco}")
        elif opcao == 5:
            novo_nome = obter_input("Digite o novo nome: ")
            novo_idade = obter_input("Digite a nova idade: ", int)
            novo_contato = obter_input("Digite o novo contato: ")
            novo_endereco = obter_input("Digite o novo endereço: ")
            cliente.nome = novo_nome
            cliente.idade = novo_idade
            cliente.contato = novo_contato
            cliente.endereco = novo_endereco
            session.commit()
            print(f"\nDados atualizados para: Nome: {novo_nome}, Idade: {novo_idade}, Contato: {novo_contato}, Endereço: {novo_endereco}")
        elif opcao == 0:
            main()
        else:
            print("\nOpção inválida. Tente novamente.")
            Cliente.editar_cliente(session, cpf)

        menu_saida()

    def excluir_cliente(session, cpf):
        cliente = session.query(Cliente).filter_by(cpf=cpf).first()
        if not cliente:
            raise ElementoNaoEncontradoError(f"\nErro: O cliente '{cpf}' não foi encontrado.")

        print(f"\nCPF: {cliente.cpf}")
        print(f"Nome: {cliente.nome}")
        print(f"Idade: {cliente.idade}")
        print(f"Contato: {cliente.contato}")
        print(f"Endereço: {cliente.endereco}")

        print("\nDeseja realmente excluir o cliente?")
        print("========================================")
        print("1 - Excluir")
        print("0 - Voltar ao menu principal")
        print("========================================")

        opcao = obter_input("Escolha uma opção: ", int)

        if opcao == 1:
            session.delete(cliente)
            session.commit()
            print(f"\nCliente '{cpf}' excluido com sucesso!")
        elif opcao == 0:
            main()
        else:
            limpar_tela()
            print("\nOpção inválida. Tente novamente.")
            Cliente.excluir_cliente(session, cpf)
            
class Diretor(db.Model):
    __tablename__ = 'diretores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_diretor = db.Column(db.String(100), nullable=False)

    filmes = relationship("Filme", back_populates="diretor")

    def cadastrar_diretor(nome):
        diretor_existente = db.session.query(Diretor).filter_by(nome_diretor = nome).first()
        if diretor_existente:
            raise ElementoExistenteError(f"\nErro: O nome '{nome}' é um diretor existente.")

        novo_diretor = Diretor(nome_diretor = nome)
        db.session.add(novo_diretor)
        print(f"\nDiretor '{nome}' criado com sucesso!")
        db.session.commit()
        
        return novo_diretor

    def consultar_diretor(session, nome_diretor):
        diretor = session.query(Diretor).filter_by(nome_diretor=nome_diretor).first()
        if not diretor:
            raise ElementoNaoEncontradoError(f"\nErro: O diretor '{nome_diretor}' não foi encontrado.")
        
        print(f'\nFilmes dirigidos por: {diretor.nome_diretor}')
        for filme in diretor.filmes:
            print(filme.nome_filme)

        menu_saida()

    def listar_diretores(session):
        diretores = session.query(Diretor).order_by(Diretor.nome_diretor).all()
        if diretores:
            print("\nDiretores:")
            for diretor in diretores:
                print(f"ID: {diretor.id}, Nome: {diretor.nome_diretor}")
        else:
            raise ElementoNaoEncontradoError("\nNenhum diretor encontrado.")

        menu_saida()

class Produtora(db.Model):
    __tablename__ = 'produtoras'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produtora = db.Column(db.String(100), nullable=False)

    filmes = relationship("Filme", back_populates="produtora")

    def cadastrar_produtora(nome):
        produtora_existente = db.session.query(Produtora).filter_by(nome_produtora = nome).first()
        if produtora_existente:
            raise ElementoExistenteError(f"\nErro: A produtora '{nome}' já existe.")

        nova_produtora = Produtora(nome_produtora = nome)
        db.session.add(nova_produtora)
        print(f"\nProdutora '{nome}' criada com sucesso!")
        db.session.commit()

        return nova_produtora

    def consultar_produtora(session, nome_produtora):
        produtora = session.query(Produtora).filter_by(nome_produtora=nome_produtora).first()
        if not produtora:
            raise ElementoNaoEncontradoError(f"\nErro: A produtora '{nome_produtora}' não foi encontrada.")
        
        print(f'\nFilmes produzidas por: {produtora.nome_produtora}')
        for filme in produtora.filmes:
            print(filme.nome_filme)

        menu_saida()

    def listar_produtoras(session):
        produtoras = session.query(Produtora).order_by(Produtora.nome_produtora).all()
        if produtoras:
            print("\nProdutoras:")
            for produtora in produtoras:
                print(f"ID: {produtora.id}, Nome: {produtora.nome_produtora}")
        else:
            raise ElementoNaoEncontradoError("\nNenhuma produtora encontrada.")

        menu_saida()

class Filme(db.Model):
    __tablename__ = 'filmes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_filme = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(60), nullable=False)
    classificacao = db.Column(db.String(10), nullable=False)
    ano_estreia = db.Column(db.Integer, nullable=False)
    sinopse = db.Column(db.String(500), nullable=True)   
    disponivel = db.Column(db.Boolean, default=True)

    diretor_id = db.Column(db.Integer, ForeignKey('diretores.id'), nullable=False)
    produtora_id = db.Column(db.Integer, ForeignKey('produtoras.id'), nullable=False)

    diretor = relationship("Diretor", back_populates="filmes")
    produtora = relationship("Produtora", back_populates="filmes")
    alugueis = relationship("Aluguel", back_populates="filme")


    def cadastrar_filme(session, nome_filme, genero, ano_estreia, classificacao, sinopse, nome_diretor, nome_produtora):
        diretor = session.query(Diretor).filter_by(nome_diretor=nome_diretor).first()
        produtora = session.query(Produtora).filter_by(nome_produtora=nome_produtora).first()
        filme_existente = session.query(Filme).filter_by(nome_filme=nome_filme).first()

        if not diretor:
            Diretor.cadastrar_diretor(nome_diretor)
            diretor = session.query(Diretor).filter_by(nome_diretor=nome_diretor).first()
        
        if not produtora:
            Produtora.cadastrar_produtora(nome_produtora)
            produtora = session.query(Produtora).filter_by(nome_produtora=nome_produtora).first()

        if not diretor:
            raise ElementoNaoEncontradoError(f"\nErro: Diretor '{nome_diretor}' não encontrado.")
        
        if not produtora:
            raise ElementoNaoEncontradoError(f"\nErro: Produtora '{nome_produtora}' não encontrada.")

        if filme_existente:
            raise ElementoExistenteError(f"\nErro: O filme '{nome_filme}' já está cadastrado.")

        novo_filme = Filme(nome_filme=nome_filme, genero=genero, ano_estreia=ano_estreia,
                            classificacao=classificacao, sinopse=sinopse, diretor=diretor, produtora=produtora)
        session.add(novo_filme)
        session.commit()
        print(f"\nFilme '{nome_filme}' cadastrado com sucesso!")
        
        menu_saida()

    def consultar_filme(session, nome_filme):
        filme = session.query(Filme).filter_by(nome_filme=nome_filme).first()
        if not filme:
            raise ElementoNaoEncontradoError(f"\nErro: O filme '{nome_filme}' não foi encontrado.")
        
        print(f"\nId: {filme.id}")
        print(f"Filme: {filme.nome_filme}")
        print(f"Genero: {filme.genero}")
        print(f"Ano de Estreia: {filme.ano_estreia}")
        print(f"Classificação: {filme.classificacao}")
        print(f"Sinopse: {filme.sinopse}")
        print(f"Diretor: {filme.diretor.nome_diretor}")
        print(f"Produtora: {filme.produtora.nome_produtora}")

        menu_saida()

    def listar_filmes_disponiveis(session):
        filmes_disponiveis = session.query(Filme).filter_by(disponivel=True).all()
        if filmes_disponiveis:
            print("\nFilmes disponíveis:")
            for filme in filmes_disponiveis:
                print(f"ID: {filme.id}, Nome: {filme.nome_filme}, Classificação: {filme.classificacao}")
        else:
            raise ElementoNaoEncontradoError("Nenhum filme disponível.")

        menu_saida()

    def listar_filmes(session):
        filmes = session.query(Filme).all()
        if filmes:
            print("\nFilmes:")
            for filme in filmes:
                print(f"ID: {filme.id}, Nome: {filme.nome_filme}, Classificação: {filme.classificacao}")
        else:
            raise ElementoNaoEncontradoError("\nNenhum filme encontrado.")

        menu_saida()

    def excluir_filme(session, nome_filme):
        filme = session.query(Filme).filter_by(nome_filme=nome_filme).first()
        if not filme:
            raise ElementoNaoEncontradoError(f"\nErro: O filme '{nome_filme}' não foi encontrado.")
    
        print(f"\nFilme '{filme.nome_filme}")
        print(f"Genero: {filme.genero}")
        print(f"Classificação: {filme.classificacao}")
        print(f"Ano de Estreia: {filme.ano_estreia}")
        print(f"Sinopse: {filme.sinopse}")
        print(f"Diretor: {filme.diretor.nome_diretor}")
        print(f"Produtora: {filme.produtora.nome_produtora}")

        print("\nDeseja realmente excluir esse filme?")
        print("1 - Excluir filme")
        print("0 - Voltar ao menu principal")
        opcao = obter_input("Escolha uma opção: ")
        if opcao == '1':
            session.delete(filme)
            session.commit()
            print(f"\nFilme '{filme.nome_filme}' excluído com sucesso!")
        elif opcao == '0':
            main()
        else:
            limpar_tela()
            print("\nOpção inválida. Tente novamente.")
            Filme.excluir_filme(session, filme)
        
class Aluguel(db.Model):
    __tablename__ = 'alugueis'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor_diaria = db.Column(db.Float, nullable=False)
    data_aluguel = db.Column(db.DateTime, default=datetime.now)
    data_devolucao = db.Column(db.DateTime, default=None)
    tempo_aluguel = db.Column(db.Integer, nullable=True)
    valor = db.Column(db.Float, nullable=True)
    status = db.Column(db.Boolean, default=True)

    cliente_cpf = db.Column(db.String(11), ForeignKey('clientes.cpf'), nullable=False)
    filme_id = db.Column(db.Integer, ForeignKey('filmes.id'), nullable=False)

    cliente = relationship("Cliente", back_populates="alugueis")
    filme = relationship("Filme", back_populates="alugueis")


    def fazer_aluguel(session, cliente_cpf, filme_id, valor_diaria):
        cliente = session.query(Cliente).filter_by(cpf=cliente_cpf).first()
        filme = session.query(Filme).filter_by(id=filme_id).first()
        aluguel_existente = session.query(Aluguel).filter_by(cliente_cpf=cliente_cpf, filme_id=filme_id).first()

        if not cliente:
            raise ElementoNaoEncontradoError(f"\nErro: O cliente com o CPF '{cliente_cpf}' não foi encontrado.")
        if not filme:
            raise ElementoNaoEncontradoError(f"\nErro: O filme não foi encontrado.")  
        if aluguel_existente:
            raise ElementoExistenteError(f"\nErro: O filme '{filme.nome_filme}' ja foi alugado para o cliente '{cliente.nome}'.")

        if filme and filme.disponivel:
            aluguel = Aluguel(valor_diaria=valor_diaria, cliente_cpf=cliente_cpf, filme_id=filme_id)
            filme.disponivel = False
            session.add(aluguel)
            session.commit()
            print(f"Aluguel do cliente '{cliente.nome}' para o filme '{filme.nome_filme}' efetuado com sucesso!")
            return f"Aluguel do cliente '{cliente.nome}' para o filme '{filme.nome_filme}' efetuado com sucesso!"
        else:
            raise AluguelRealizadoError(f"Erro: O filme '{filme.nome_filme}' nao esta disponivel para alugar.")

    def devolver_aluguel(session, aluguel_id):
        aluguel = session.query(Aluguel).filter_by(id=aluguel_id).one_or_none()
        if not aluguel:
            raise ElementoNaoEncontradoError(f"\nErro: O aluguel com o ID '{aluguel_id}' não foi encontrado.")
        
        if not aluguel.filme.disponivel:
            # session.delete(aluguel)
            aluguel.data_aluguel_devolucao = datetime.now()
            aluguel.tempo_aluguel = (aluguel.data_aluguel_devolucao - aluguel.data_aluguel).days
            aluguel.valor = aluguel.tempo_aluguel * aluguel.valor_diaria
            aluguel.Status = False
            aluguel.filme.disponivel = True
            print(f"\nAluguel do cliente '{aluguel.cliente.nome}' para o filme '{aluguel.filme.nome_filme}' devolvido com sucesso. Deve ser pago R$ {aluguel.valor}")
            session.commit()

            menu_saida()

    def consultar_aluguel_por_id(session, id_aluguel):
        aluguel = session.query(Aluguel).filter_by(id=id_aluguel).first()
        if aluguel:
            print(f"\nAluguel ID: {aluguel.id}")
            print(f'data_aluguel: {aluguel.data_aluguel}')
            print(f'data_aluguel_devolucao: {aluguel.data_devolucao}')
            print(f'tempo_aluguel: {aluguel.tempo_aluguel}')
            print(f'valor: {aluguel.valor}')
            print(f'status: {aluguel.status}')
        else:
            raise ElementoNaoEncontradoError("\nAluguel não encontrado.")

        menu_saida()

    def consultar_aluguel_por_cpf(session, cpf_cliente):
        alugueis_cliente = session.query(Aluguel).filter_by(cliente_cpf=cpf_cliente).all()
        if alugueis_cliente:
            print(f"\nAlugueis feitos pelo cliente com CPF {cpf_cliente}:")
            for aluguel in alugueis_cliente:
                print(f"ID: {aluguel.id}, Filme: {aluguel.filme.nome_filme}, Data: {aluguel.data_aluguel}")
        else:
            raise ElementoNaoEncontradoError("\nNenhum aluguel encontrado para este cliente.")

        menu_saida()

    def listar_filmes_alugados(session):
        filmes_alugados = session.query(Aluguel).all()
        if filmes_alugados:
            print("\nAlugueis feitos:")
            for aluguel in filmes_alugados:
                print(f"ID: {aluguel.id}, Cliente: {aluguel.cliente.nome}, Data: {aluguel.data_aluguel}, Preço: {aluguel.valor} R$")
        else:
            raise ElementoNaoEncontradoError("\nNenhum aluguel feito.")

        menu_saida()

    def alterar_aluguel(session, id_aluguel):
        limpar_tela()
        aluguel = session.query(Aluguel).filter_by(id=id_aluguel).one_or_none()
        if not aluguel:
            raise ElementoNaoEncontradoError(f"\nErro: O aluguel com o ID '{id_aluguel}' não foi encontrado.")
        
        print("Id: ", aluguel.id)
        print("Data aluguel: ", aluguel.data_aluguel)
        print("Data devolução: ", aluguel.data_devolucao)
        print("Tempo aluguel: ", aluguel.tempo_aluguel)
        print("Valor: ", aluguel.valor)
        print("Status: ", aluguel.status)

        print("\nEscolha o campo que deseja editar:")
        print("1 - Tempo aluguel")
        print("2 - Valor")
        print("3 - Status")
        print("0 - Sair")
        opcao = int(input("Escolha uma opção: "))
        limpar_tela()

        if opcao == 1:
            tempo_aluguel = int(input("Digite o novo Tempo aluguel: "))
            aluguel.tempo_aluguel = tempo_aluguel
        elif opcao == 2:
            valor = float(input("Digite o novo valor: "))            
            aluguel.valor = valor
        elif opcao == 3:
            if aluguel.status == True:
                aluguel.status = False
            else:
                aluguel.status = True
        elif opcao == 0:
            main()
        else:
            Aluguel.alterar_aluguel(session, id_aluguel)
            print("Opção inválida. Tente novamente.")
        
        session.commit()
        limpar_tela()
        print("\nAluguel editado com sucesso!")
        print("\nRealizar alterações Outras Alterações?")
        print("1 - Sim")
        print("2 - Não")
        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            Aluguel.alterar_aluguel(session, id_aluguel)
        elif opcao == 2:
            menu_saida()

       

        menu_saida()

    def excluir_aluguel(session, id_aluguel):
        aluguel = session.query(Aluguel).filter_by(id=id_aluguel).one_or_none()
        if not aluguel:
            raise ElementoNaoEncontradoError(f"\nErro: O aluguel com o ID '{id_aluguel}' não foi encontrado.")

        print(f"\nAluguel ID: {aluguel.id}")
        print(f'valor diaria: {aluguel.valor_diaria}')
        print(f'Data aluguel: {aluguel.data_aluguel}')
        print(f'Data devolucao: {aluguel.data_devolucao}')
        print(f'Tempo aluguel: {aluguel.tempo_aluguel}')
        print(f'Valor: {aluguel.valor}')
        print(f'Status: {aluguel.status}')
        print(f'Cliente Cpf: {aluguel.cliente_cpf}')
        print(f'Filme Id: {aluguel.filme_id}')

        print("\nDeseja realmente excluir o aluguel?")
        print("1 - Sim")
        print("0 - Voltar ao menu principal")
        opcao = obter_input("Escolha uma opção: ")
        if opcao == '1':
            if aluguel.status == True:
                aluguel.status = False
            session.delete(aluguel)
            session.commit()
            print("\nAluguel excluido com sucesso!")
        elif opcao == '2':
            main()
        else:
            limpar_tela ()
            print("Opção inválida. Tente novamente.")
            Aluguel.excluir_aluguel(session, id_aluguel)


def menu_saida():
    print("\n1 - Voltar ao menu principal?")
    print("2 - Sair")
    opcao = int(input("Escolha uma opção: "))
    if opcao == 1:
        limpar_tela()
        return main()
    elif opcao == 2:
        sys.exit()
    else:
        print("Opção inválida. Tente novamente.")
