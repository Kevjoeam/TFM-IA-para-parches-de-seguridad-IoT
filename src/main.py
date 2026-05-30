import os
import sys
import time

# Rutas para importar módulos
sys.path.append(os.path.join(os.getcwd(), 'src'))
from ast_engine.context_pruner import prune_vulnerable_context
from ai_connector.local_patcher import generate_local_patch
from validation.patch_validator import run_validation

def run_self_healing_loop(target_file):
    print("=== INICIANDO CICLO DE AUTORREPARACIÓN (Self-Healing) ===")
    
    # 1. DETECCIÓN (RF1)
    report_path = "data/reports/vulnerability_report.json"
    print(f"\n[1/4] Ejecutando detección SAST en {target_file}...")
    os.system(f"bandit -f json -o {report_path} {target_file} > nul 2>&1")
    
    # 2. PODA DE CONTEXTO (RF2)
    print("[2/4] Optimizando contexto mediante poda de AST...")
   # contexto, issue = prune_vulnerable_context(report_path)
    contexto, issue, ahorro = prune_vulnerable_context(report_path)

    if not contexto:
        print("No se requiere parcheo.")
        return

    # 3. GENERACIÓN DE PARCHE (RF3/RF4)
    print(f"[3/4] Solicitando parche a LLM local...")
    patch = generate_local_patch(contexto, issue['issue_text'])
    
    # 4. VALIDACIÓN EN SANDBOX (RF6)
    print("[4/4] Validando integridad del parche en Sandbox Docker...")
    success = run_validation(patch)
    
    if success:
        print("\n El parche ha sido verificado y está listo para despliegue.")
    else:
        print("\nEl parche generado no superó las pruebas de seguridad.")

if __name__ == "__main__":
    run_self_healing_loop("src/test_device.py")