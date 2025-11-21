# models/caixa.py - Registra vendas, persiste histórico e gera fechamento
import datetime
import json
import csv
import os

class Caixa:
    # Construtor: define arquivos de persistência para histórico de vendas
    def __init__(self, arquivo_vendas: str = "data/vendas.json", arquivo_vendas_csv: str = "data/vendas.csv"):
        self._total_dia = 0.0
        self._itens_vendidos = 0
        self.arquivo_vendas = arquivo_vendas
        self.arquivo_vendas_csv = arquivo_vendas_csv
        # Garante que o CSV tenha cabeçalho caso não exista
        if not os.path.exists(self.arquivo_vendas_csv):
            os.makedirs(os.path.dirname(self.arquivo_vendas_csv), exist_ok=True)
            with open(self.arquivo_vendas_csv, "w", encoding="utf-8", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["data_hora", "total", "itens", "forma", "cupom"])

    # Registra a venda atualizando totais e salvando histórico
    def registrar_venda(self, total_compra: float, itens_vendidos: int, forma: str, cupom: str = None):
        # Atualiza totais em memória
        self._total_dia += float(total_compra)
        self._itens_vendidos += int(itens_vendidos)
        # Cria registro da venda
        venda = {
            "data_hora": datetime.datetime.now().isoformat(),
            "total": float(total_compra),
            "itens": int(itens_vendidos),
            "forma": forma,
            "cupom": cupom
        }
        # Garante existência da pasta do arquivo JSON
        os.makedirs(os.path.dirname(self.arquivo_vendas), exist_ok=True)
        # Carrega vendas já existentes (se houver)
        vendas = []
        if os.path.exists(self.arquivo_vendas):
            try:
                with open(self.arquivo_vendas, "r", encoding="utf-8") as f:
                    vendas = json.load(f)
            except Exception:
                vendas = []
        # Adiciona a nova venda e salva o JSON
        vendas.append(venda)
        with open(self.arquivo_vendas, "w", encoding="utf-8") as f:
            json.dump(vendas, f, ensure_ascii=False, indent=2)
        # Adiciona linha no CSV também
        with open(self.arquivo_vendas_csv, "a", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([venda["data_hora"], venda["total"], venda["itens"], venda["forma"], venda["cupom"]])

    # Gera o fechamento do caixa em arquivo TXT e imprime no console
    def fechamento(self, pasta_reports: str = "reports") :
        # Formata timestamp para nome do arquivo
        agora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Define o caminho do arquivo de fechamento
        nome_arquivo = os.path.join(pasta_reports, f"fechamento_{agora}.txt")
        # Garante que a pasta exista
        os.makedirs(os.path.dirname(nome_arquivo), exist_ok=True)
        # Escreve o conteúdo do relatório
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write("===== FECHAMENTO DO CAIXA =====\n")
            f.write(f"Total arrecadado no dia: R$ {self._total_dia:.2f}\n")
            f.write(f"Total de itens vendidos: {self._itens_vendidos}\n")
            f.write("===============================\n")
        # Imprime no console o resumo do fechamento
        print("===== FECHAMENTO DO CAIXA =====")
        print(f"Total arrecadado no dia: R$ {self._total_dia:.2f}")
        print(f"Total de itens vendidos: {self._itens_vendidos}")
        print(f"Relatório salvo em: {nome_arquivo}")
