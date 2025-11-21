# models/pagamento.py - Processamento de pagamento com cupons
class Pagamento:
    # Construtor: recebe total bruto e cupom (opcional)
    def __init__(self, total: float, cupom: str = None):
        self._total = float(total)
        self.cupom = cupom
        self.valor_final = 0.0
        self.descricao = ""

    # Calcula o valor final com base na forma de pagamento e cupom
    def calcular_pagamento(self, opcao: int):
        if opcao == 1:
            self.valor_final = self._total * 0.90
            self.descricao = "Dinheiro/PIX - 10% desconto"
        elif opcao == 2:
            self.valor_final = self._total * 0.95
            self.descricao = "Cartão de Débito - 5% desconto"
        elif opcao == 3:
            self.valor_final = self._total
            self.descricao = "Crédito 1x - sem desconto"
        elif opcao == 4:
            self.valor_final = self._total * 1.05
            self.descricao = "Crédito 2x - +5%"
        elif opcao == 5:
            self.valor_final = self._total * 1.10
            self.descricao = "Crédito 3x - +10%"
        elif opcao == 6:
            self.valor_final = self._total * 1.15
            self.descricao = "Crédito 4x - +15%"
        else:
            raise ValueError("Opção inválida de pagamento.")

        # Aplica cupom se fornecido (ex.: CUPOM10)
        if self.cupom:
            cupom = str(self.cupom).strip().upper()
            if cupom == "CUPOM10": 
                self.valor_final *= 0.90
                self.descricao += " + Cupom CUPOM10 (10% off)"
            elif cupom == "CUPOM5":
                self.valor_final *= 0.95
                self.descricao += " + Cupom CUPOM5 (5% off)"
            else:
                # Cupom inválido é apenas ignorado (poderia ser levantada exceção)
                self.descricao += " + Cupom inválido (ignorado)"
