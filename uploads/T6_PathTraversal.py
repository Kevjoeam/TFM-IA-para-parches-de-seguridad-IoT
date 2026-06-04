# src/T4_PathTraversal.py
from pathlib import Path

BASE_DIR = Path("/etc/config")

def read_file(filename):
    path = BASE_DIR / filename

    with open(path, "r") as f:
        return f.read()