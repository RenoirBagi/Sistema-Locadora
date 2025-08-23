class ElementoExistenteError(Exception):
    pass

class ElementoNaoEncontradoError(Exception):
    pass

class MenorDeIdadeError(Exception):
    pass

class AluguelRealizadoError(Exception):
    pass

def obter_input(mensagem, tipo=str):
    while True:
        try:
            valor = input(mensagem)
            if not valor.strip(): 
                raise ValueError("\nValor não pode ser vazio.\n")
            valor_convertido = tipo(valor)
            return valor_convertido
        except ValueError as e:
            print(e)

def menu_input(mensagem, tipo=str):
    while True:
        try:
            valor = input(mensagem)
            if not valor.strip(): 
                raise ValueError("\nValor não pode ser vazio.\n")
            valor_convertido = tipo(valor)
            return valor_convertido
        except ValueError as e:
            print(e)
