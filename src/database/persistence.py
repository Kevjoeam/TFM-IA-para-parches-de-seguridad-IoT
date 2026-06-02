import os
import json
from datetime import datetime

def log_remediation_event(vulnerability, line, ahorro, patch_code, success):

    event_data = {
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Vulnerabilidad": vulnerability,
        "Línea": line,
        "Reducción Contexto": f"{ahorro}%",
        "Parche": patch_code[:100] + "...",
        "Resultado": "VALIDADO" if success else "FALLIDO"
    }

    # Ruta para guardar en la carpeta data/reports
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    report_dir = os.path.join(base_path, "data", "reports")
    file_path = os.path.join(report_dir, "audit_history.json")

    os.makedirs(report_dir, exist_ok=True)

    history = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except: history = []

    history.insert(0, event_data) 
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)
    
    return True