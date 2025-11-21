# utils/io_helpers.py - Funções auxiliares para ler e validar entrada do usuário
def ler_inteiro(mensagem: str) -> int:
    # Loop até receber um inteiro válido
    while True:
        try:
            # Lê a entrada e tenta converter para inteiro
            return int(input(mensagem).strip())
        except ValueError:
            # Informa que a entrada não é válida e repete
            print("Digite um número inteiro válido.")

def ler_float(mensagem: str) -> float:
    # Loop até receber um float válido
    while True:
        try:
            # Lê e converte para float
            return float(input(mensagem).strip())
        except ValueError:
            # Mensagem de erro e repete
            print("Digite um número válido (ex.: 12.50).")

def ler_texto(mensagem: str) -> str:
    # Lê texto e remove espaços extras nas extremidades
    return input(mensagem).strip()
