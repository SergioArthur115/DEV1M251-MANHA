# main.py - Ponto de entrada do sistema
# Importa a classe Sistema do módulo controllers.sistema
from controllers.sistema import Sistema

# Função que exibe o menu principal e controla escolhas do usuário
def menu_principal():
    # Cria a instância do Sistema (carrega produtos e configura o caixa)
    sistema = Sistema()

    # Loop principal do programa (executa até o usuário escolher sair)
    while True:
        # Exibe o cabeçalho do menu
        print("\n===== SISTEMA DO MERCADO - VERSÃO CORRIGIDA =====")
        # Opção para gerenciar produtos
        print("[1] Gerenciar produtos (adicionar / listar / editar)")
        # Opção para abrir o caixa (atender clientes)
        print("[2] Abrir caixa e iniciar atendimento")
        # Opção para sair do programa
        print("[3] Fechar programa")

        # Lê a opção do usuário (string) e remove espaços em branco
        opc = input("Escolha uma opção: ").strip()

        # Se usuário escolher 1, chama o menu de gerenciamento de produtos
        if opc == "1":
            sistema.menu_gerenciar_produtos()
        # Se usuário escolher 2, abre o caixa para atender clientes
        elif opc == "2":
            sistema.abrir_caixa_e_atender()
        # Se usuário escolher 3, encerra o loop e finaliza o programa
        elif opc == "3":
            print("Encerrando o sistema. Até mais!")
            break
        # Qualquer outra entrada é inválida e solicita nova tentativa
        else:
            print("Opção inválida. Escolha 1, 2 ou 3.")

# Garante que o menu só rode quando este arquivo for executado diretamente
if __name__ == "__main__":
    menu_principal()
