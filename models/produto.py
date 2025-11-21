# models/produto.py - Representação de um produto e gestão de estoque
# Define a classe Produto com atributos e métodos para manipular estoque

class Produto:
    # Construtor: cria um produto com código, nome, preço, estoque e estoque mínimo
    def __init__(self, codigo: int, nome: str, preco: float, estoque: int = 10, estoque_minimo: int = 2):
        # Código identificador do produto (inteiro)
        self._codigo = int(codigo)
        # Nome do produto (string)
        self._nome = str(nome)
        # Preço unitário (float)
        self._preco = float(preco)
        # Quantidade em estoque (inteiro)
        self._estoque = int(estoque)
        # Estoque mínimo que dispara alerta (inteiro)
        self._estoque_minimo = int(estoque_minimo)

    # Propriedade para ler o código do produto
    @property
    def codigo(self) -> int:
        return self._codigo

    # Propriedade para ler o nome do produto
    @property
    def nome(self) -> str:
        return self._nome

    # Propriedade para ler o preço do produto
    @property
    def preco(self) -> float:
        return self._preco

    # Propriedade para ler a quantidade em estoque
    @property
    def estoque(self) -> int:
        return self._estoque

    # Propriedade para ler o estoque mínimo configurado
    @property
    def estoque_minimo(self) -> int:
        return self._estoque_minimo

    # Método para reduzir o estoque (usado ao adicionar ao carrinho)
    def reduzir_estoque(self, quantidade: int):
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva.")
        if quantidade > self._estoque:
            raise ValueError(f"⚠ Estoque insuficiente! Disponível: {self._estoque}")
        self._estoque -= quantidade

    # Método para aumentar o estoque (ex.: remoção do carrinho)
    def aumentar_estoque(self, quantidade: int):
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva.")
        self._estoque += quantidade

    # Atualiza o estoque para um valor específico
    def atualizar_estoque(self, nova_quantidade: int):
        nova_quantidade = int(nova_quantidade)
        if nova_quantidade < 0:
            raise ValueError("Estoque não pode ser negativo.")
        self._estoque = nova_quantidade

    # Atualiza o estoque mínimo
    def atualizar_estoque_minimo(self, novo_minimo: int):
        novo_minimo = int(novo_minimo)
        if novo_minimo < 0:
            raise ValueError("Estoque mínimo não pode ser negativo.")
        self._estoque_minimo = novo_minimo

    # Indica se o produto está com estoque baixo
    def estoque_baixo(self) -> bool:
        return self._estoque <= self._estoque_minimo

    # Representação em string do produto para exibição no terminal
    def __str__(self) -> str:
        return f"[{self._codigo}] {self._nome} - R$ {self._preco:.2f} (Estoque: {self._estoque})"

    # ** CORREÇÃO APLICADA AQUI: Adiciona __eq__ e __hash__ para que o Carrinho funcione corretamente **
    def __eq__(self, other):
        if isinstance(other, Produto):
            return self._codigo == other._codigo
        return False

    def __hash__(self) -> int:
        return hash(self._codigo)
    # ** FIM DA CORREÇÃO **

    # Converte o produto em dicionário para salvar em JSON
    def to_dict(self) -> dict:
        return {
            "codigo": self._codigo,
            "nome": self._nome,
            "preco": self._preco,
            "estoque": self._estoque,
            "estoque_minimo": self._estoque_minimo
        }

    # Cria um Produto a partir de um dicionário (útil ao carregar JSON)
    @staticmethod
    def from_dict(d: dict):
        return Produto(d["codigo"], d["nome"], d["preco"], d.get("estoque", 0), d.get("estoque_minimo", 2))