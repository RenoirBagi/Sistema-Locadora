def main():
    from Classes import Cliente, Filme, Aluguel, Diretor, Produtora
    from Error import ElementoExistenteError, ElementoNaoEncontradoError, AluguelRealizadoError, MenorDeIdadeError, obter_input
    from Config import session, limpar_tela
    import sys

    while True:
        print("\nBem-vindo ao sistema de locadora de filmes!")
        print("Escolha uma das opções:")
        print("========================================")
        print("1 - Cadastrar")            
        print("2 - Consultar")           
        print("3 - Aluguel")    
        print("4 - Listar")
        print("5 - Alterar")
        print("6 - Excluir")
        print("0 - Sair")
        print("========================================")

        opcao = obter_input("Escolha uma opção: ", int)

        if opcao == 1: #CADASTRAR
            limpar_tela()
            print("\nEscolha uma das opções:")
            print("========================================")
            print("1 - Cadastrar cliente")
            print("2 - Cadastrar diretor")    
            print("3 - Cadastrar produtora")    
            print("4 - Cadastrar filme")
            print("0 - Voltar ao menu principal")
            print("========================================")

            opcao_cadastrar = obter_input("Escolha uma opção: ", int)

            try:
                if opcao_cadastrar == 1:
                    limpar_tela()
                    nome = obter_input("\nDigite o nome do cliente: ")
                    idade = obter_input("Digite a idade do cliente: ", int)
                    while idade < 18:
                        print("\nOps, parece que o apressadinho não tem 18 anos!")
                        print("Opção 1 - Digitar outra idade?")
                        print("Opção 2 - Voltar ao menu principal")
                        opcao = obter_input("Escolha uma opção: ", int)
                        if opcao == 1:
                            idade = obter_input("\nDigite a idade do cliente: ", int)
                        elif opcao == 2:
                            main()
                        # else:
                        #     limpar_tela()
                        #     print("Opção inválida. Tente novamente.")                    
                    cpf = obter_input("Digite o CPF do cliente: ")
                    contato = obter_input("Digite o contato do cliente: ")
                    endereco = obter_input("Digite o endereço do cliente: ")
                    Cliente.cadastrar_cliente(cpf, nome, idade, contato, endereco)

                elif opcao_cadastrar == 2:
                    limpar_tela()
                    nome_diretor = obter_input("Digite o nome do diretor: ")
                    Diretor.cadastrar_diretor(nome_diretor)

                elif opcao_cadastrar == 3:
                    limpar_tela()
                    nome_produtora = obter_input("Digite o nome da produtora: ")
                    Produtora.cadastrar_produtora(nome_produtora)

                elif opcao_cadastrar == 4:
                    limpar_tela()
                    nome_filme = obter_input("Digite o nome do filme: ")
                    genero = obter_input("Digite o gênero do filme: ")
                    ano_estreia = obter_input("Digite o ano de estreia do filme: ", int)
                    classificacao = obter_input("Digite a classificação indicativa do filme: ")
                    sinopse = obter_input("Digite a sinopse do filme: ")
                    diretor = obter_input("Digite o nome do diretor do filme: ")
                    produtora = obter_input("Digite o nome da produtora do filme: ")
                    Filme.cadastrar_filme(session, nome_filme, genero, ano_estreia, classificacao, sinopse, diretor, produtora)
                
                elif opcao_cadastrar == "0":
                    limpar_tela()
                    main()
                
                else:
                    limpar_tela()
                    print("Opção inválida. Tente novamente.")

            except ElementoExistenteError as e:
                print(e)

            except ElementoNaoEncontradoError as e:
                print(e)

            except MenorDeIdadeError as e:
                print(e)

            except ValueError as e:
                print(e)

        elif opcao == 2: #CONSULTAR
            limpar_tela()
            print("\nEscolha uma das opções:")
            print("========================================")
            print("1 - Consultar cliente")
            print("2 - Consultar filme")    
            print("3 - Consultar diretor")
            print("4 - Consultar produtora")
            print("5 - Consultar alugueis")
            print("0 - Voltar ao menu principal")
            print("========================================")

            opcao_consultar = obter_input("Escolha uma opção: ", int)
            
            try:

                if opcao_consultar == 1:
                    limpar_tela()
                    cpf = obter_input("\nDigite o CPF do cliente: ")
                    
                    Cliente.consultar_cliente(session, cpf)

                elif opcao_consultar == 2:
                    limpar_tela()
                    nome_filme = obter_input("Digite o nome do filme: ")
                    Filme.consultar_filme(session, nome_filme)

                elif opcao_consultar == 3:
                    limpar_tela()
                    nome_diretor = obter_input("Digite o nome do diretor: ")
                    Diretor.consultar_diretor(session, nome_diretor)

                elif opcao_consultar == 4:
                    limpar_tela()
                    nome_produtora = obter_input("Digite o nome da produtora: ")
                    Produtora.consultar_produtora(session, nome_produtora)
                
                elif opcao_consultar == 5:
                    limpar_tela()
                    print("\nConsultar aluguel:")
                    print("========================================")
                    print("1. Consultar por ID do Aluguel")
                    print("2. Consultar por CPF do Cliente")
                    print("0. Voltar para menu principal")
                    print("========================================")
                    opcao_consulta_aluguel = obter_input("Escolha uma opção: ")

                    if opcao_consulta_aluguel == "1":
                        # Consultar por ID do Aluguel
                        limpar_tela()
                        id_aluguel_consulta = obter_input("ID do aluguel: ", int)
                        Aluguel.consultar_aluguel_por_id(session, id_aluguel_consulta)

                    elif opcao_consulta_aluguel == "2":
                        # Consultar por CPF do Cliente
                        limpar_tela()
                        cpf_consulta = obter_input("CPF do cliente (somente números): ")
                        Aluguel.consultar_aluguel_por_cpf(session, cpf_consulta)
                    
                    elif opcao_consulta_aluguel == "0":
                        limpar_tela()
                        main()

                    else:
                        limpar_tela()
                        print("Opção inválida. Tente novamente.")

                elif opcao == 0:
                    limpar_tela()
                    main()
                
                else:
                    limpar_tela()
                    print("Opção inválida. Tente novamente.")

            except ElementoNaoEncontradoError as e:
                print(e)

        elif opcao == 3: #ALUGAR
            limpar_tela()
            print("Escolha uma das opções:")
            print("========================================")
            print("1 - Alugar filme")
            print("2 - Devolver filme")    
            print("0 - Voltar ao menu principal")
            print("========================================")

            opcao_alugar = obter_input("Escolha uma opção: ", int)

            try:
                if opcao_alugar == 1:
                    limpar_tela()
                    cliente_cpf = obter_input("Digite o CPF do cliente: ")
                    filme = obter_input("Digite o id do filme: ")
                    valor_diaria = obter_input("Digite o valor da diaria do aluguel: ", float)
                    Aluguel.fazer_aluguel(session, cliente_cpf, filme, valor_diaria)
                
                elif opcao_alugar == 2:
                    limpar_tela()
                    aluguel_id = obter_input("Digite o ID do aluguel: ",int)
                    Aluguel.devolver_aluguel(session, aluguel_id)

                elif opcao_alugar == 0:
                    limpar_tela()
                    main()

                else:
                    limpar_tela()
                    print("Opção inválida. Tente novamente.")

            except ElementoNaoEncontradoError as e:
                print(e)

            except ElementoExistenteError as e:
                print(e)

            except AluguelRealizadoError as e:
                print(e)

        elif opcao == 4: #LISTAR
            limpar_tela()
            print("\nEscolha uma das opções:")
            print("========================================")
            print("1 - Listar clientes")
            print("2 - Listar filmes")
            print("3 - Listar filmes disponíveis")
            print("4 - Listar filmes alugados")
            print("5 - Listar diretores")
            print("6 - Listar produtoras")
            print("0 - Voltar ao menu principal")
            print("========================================")

            opcao_listar = obter_input("Escolha uma opção: ", int)

            try:
                if opcao_listar == 1:
                    limpar_tela()
                    Cliente.listar_clientes(session)
            
                elif opcao_listar == 2:
                    limpar_tela()
                    Filme.listar_filmes(session)

                elif opcao_listar== 3:
                    limpar_tela()
                    Filme.listar_filmes_disponiveis(session)

                elif opcao_listar == 4:
                    limpar_tela()
                    Aluguel.listar_filmes_alugados(session)

                elif opcao_listar == 5:
                    limpar_tela()
                    Diretor.listar_diretores(session)

                elif opcao_listar == 6:
                    limpar_tela()
                    Produtora.listar_produtoras(session)

                elif opcao_listar == 0:
                    limpar_tela()
                    main()

                else:
                    limpar_tela()
                    print("Opção inválida. Tente novamente.")

            except ElementoNaoEncontradoError as e:
                print(e)
        
        elif opcao == 5: #ALTERAR
            limpar_tela()
            print("\nEscolha uma das opções:")
            print("========================================")
            print("1 - Alterar cliente")
            print("2 - Alterar aluguel")
            print("0 - Voltar ao menu principal")
            print("========================================")

            opcao_alterar = obter_input("Escolha uma opção: ", int)

            try:
                if opcao_alterar == 1:
                    limpar_tela()
                    cpf = obter_input("Digite o CPF do cliente: ")
                    Cliente.alterar_cliente(session, cpf)

                elif opcao_alterar == 2:
                    limpar_tela()
                    aluguel_id = obter_input("Digite o ID do aluguel: ",int)
                    Aluguel.alterar_aluguel(session, aluguel_id)

                elif opcao_alterar == 0:
                    limpar_tela()
                    main()

                else:
                    limpar_tela()
                    print("Opção inválida. Tente novamente.")

            except ElementoNaoEncontradoError as e:
                print(e)

        elif opcao == 6: #EXCLUIR
            limpar_tela()
            print("\nEscolha uma das opções:")
            print("========================================")
            print("1 - Excluir cliente")
            print("2 - Excluir filme")
            print("3 - Excluir aluguel")
            print("0 - Voltar ao menu principal")
            print("========================================")

            opcao_excluir = obter_input("Escolha uma opção: ", int)

            try:
                if opcao_excluir == 1:
                    limpar_tela()
                    cpf = obter_input("Digite o CPF do cliente: ", str)
                    Cliente.excluir_cliente(session, cpf)

                elif opcao_excluir == 2:
                    limpar_tela()
                    nome_filme = obter_input("Digite o nome do filme: ", str)
                    Filme.excluir_filme(session, nome_filme)

                elif opcao_excluir == 3:
                    limpar_tela()
                    id_aluguel = obter_input("Digite o ID do aluguel: ", int)
                    Aluguel.excluir_aluguel(session, id_aluguel)
                
                elif opcao == 0: #SAIR
                    limpar_tela()
                    main()

                else:
                    limpar_tela()
                    print("Opção inválida. Tente novamente.")

            except ElementoNaoEncontradoError as e:
                print(e)

        elif opcao == 0: #SAI
            sys.exit()

        else:
            limpar_tela()
            print("\nOpção inválida. Tente novamente.")
            main()


if __name__ == "__main__":
    main()