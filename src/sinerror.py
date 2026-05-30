# src/firmware_service.py
def get_config(filename):
    # VULNERABILIDAD: Path Traversal
    with open("/etc/config/" + filename, "r") as f:
        return f.read()