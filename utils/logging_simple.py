# utils/logging_simple.py - logging simples para registrar eventos/erros
import datetime
import os

# Caminho para o arquivo de log
LOG_FILE = "logs/log.txt"

# Função que escreve uma linha de log com timestamp
def log(text: str):
    # Garante que a pasta exista
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    # Abre o arquivo em modo append e escreve a mensagem com timestamp
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now().isoformat()} - {text}\n")
