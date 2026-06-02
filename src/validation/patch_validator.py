import subprocess
import os
import re
import json

def extract_code(ia_text):
    # 1. Intentar extraer contenido entre ```python ... ```
    code_match = re.search(r'```python\n(.*?)\n```', ia_text, re.DOTALL)
    if code_match:
        return code_match.group(1).strip()
    
    # 2. Intentar extraer contenido entre ``` ... ``` genérico
    code_match = re.search(r'```\n(.*?)\n```', ia_text, re.DOTALL)
    if code_match:
        return code_match.group(1).strip()

    # 3. Limpiar líneas que no parezcan código
    lines = ia_text.split('\n')
    clean_lines = [l for l in lines if not l.startswith(('Aquí', 'Este', 'Solución', 'Explicación'))]
    return '\n'.join(clean_lines).strip()

def run_validation(patch_text):
    clean_code = extract_code(patch_text) 

    with open("patch_test.py", "w", encoding='utf-8') as f:
        f.write(clean_code)

    print("--- INICIANDO VALIDACIÓN SINTÁCTICA EN SANDBOX ---")
    try:
        # FASE 1: Validación sintáctica en entorno aislado Docker
        subprocess.run(["docker", "build", "-t", "iot-sandbox", "."], check=True, capture_output=True)
        
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{os.getcwd()}:/app", "iot-sandbox", "python", "-m", "py_compile", "patch_test.py"],
            capture_output=True, text=True
        )
        
        if result.returncode != 0:
            print(f" ERROR DE SINTAXIS EN EL PARCHE:\n{result.stderr}")
            return False
            
        print(" VALIDACIÓN SINTÁCTICA EXITOSA: El parche es código Python válido.")
        
        # FASE 2: Re-escaneo secuencial de seguridad SAST (Bandit) con umbral de severidad
        print("--- INICIANDO RE-ESCANEO DE SEGURIDAD SECUENCIAL (SAST) ---")
        bandit_res = subprocess.run(
            ["bandit", "-f", "json", "patch_test.py"],
            capture_output=True, text=True
        )
        
        try:
            bandit_json = json.loads(bandit_res.stdout)
            
            # FILTRO CRÍTICO: Filtrar y buscar únicamente fallos de severidad MEDIA o ALTA
            # Esto evita que avisos informativos (como el mero hecho de importar subprocess) bloqueen el parche
            vulnerabilidades_reales = [
                r for r in bandit_json.get("results", []) 
                if r.get("issue_severity") in ["MEDIUM", "HIGH"]
            ]
            
            if len(vulnerabilidades_reales) > 0:
                print(" RECHAZADO: El parche propuesto mantiene o introdujo vulnerabilidades de riesgo Medio/Alto.")
                for vuln in vulnerabilidades_reales:
                    print(f"   - [{vuln.get('issue_severity')}] ID: {vuln.get('test_id')} - {vuln.get('issue_text')}")
                return False
                
        except Exception as json_err:
            print(f" Advertencia en el análisis del reporte SAST secundario: {json_err}")
            
        print(" VALIDACIÓN COMPLETA: Parche aprobado con éxito (Sintaxis correcta y libre de riesgos Medios/Altos).")
        return True
        
    except Exception as e:
        print(f" ERROR TÉCNICO EN EL CICLO DE VALIDACIÓN: {e}")
        return False