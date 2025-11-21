import datetime
import os

log_file = "logs/log.txt"


def log(text: str):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "a", encoding="utf=8") as f:
        f.write(f"{datetime.datetime.now().isoformat()} - {text}\n")
