from pathlib import Path

BASE_DIR = Path("/etc/config")

def get_config(filename):

    file_path = (BASE_DIR / filename).resolve()

    if not str(file_path).startswith(str(BASE_DIR)):
        raise ValueError("Ruta inválida")

    with open(file_path, "r") as f:
        return f.read()