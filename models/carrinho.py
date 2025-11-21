# models/carrinho.py - Gerencia os itens do carrinho do cliente
from models.produto import Produto

class Carrinho:
    # Construtor: cria um dicionário privado para armazenar itens (Produto->quantidade)
    def __init__(self):
        self.__itens = {}

    # Adiciona produto ao carrinho e reduz estoque do produto
    def adicionar(self, produto: Produto, quantidade: int):
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")
        # Chama o método do produto para reduzir o estoque (valida disponibilidade)
        produto.reduzir_estoque(quantidade)
        # Soma quantidade se já existir no carrinho, caso contrário cria entrada
        if produto in self.__itens:
            self.__itens[produto] += quantidade
        else:
            self.__itens[produto] = quantidade

    # Remove unidades do carrinho e devolve ao estoque do produto
    def remover(self, produto: Produto, quantidade: int):
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("Quantidade inválida.")
        if produto in self.__itens:
            qtd_no_carrinho = self.__itens[produto]
            if quantidade >= qtd_no_carrinho:
                produto.aumentar_estoque(qtd_no_carrinho)
                del self.__itens[produto]
            else:
                self.__itens[produto] -= quantidade
                produto.aumentar_estoque(quantidade)

    # Retorna itens como iterável de pares (produto, quantidade)
    def listar_itens(self):
        return self.__itens.items()

    # Calcula o total do carrinho
    def calcular_total(self) -> float:
        return sum(produto.preco * qtd for produto, qtd in self.__itens.items())

    # Retorna número total de unidades no carrinho
    def total_itens(self) -> int:
        return sum(qtd for qtd in self.__itens.values())

    # Indica se o carrinho está vazio
    def vazio(self) -> bool:
        return len(self.__itens) == 0
