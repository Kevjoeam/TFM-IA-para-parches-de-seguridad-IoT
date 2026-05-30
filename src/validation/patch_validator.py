import subprocess
import os
import re

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
    """
    Valida que el parche sea sintácticamente correcto en un entorno aislado (RF6)[cite: 304].
    """
    # Extractor de código mejorado para limpiar la respuesta
    clean_code = extract_code(patch_text) 

    with open("patch_test.py", "w", encoding='utf-8') as f:
        f.write(clean_code)

    print("--- INICIANDO VALIDACIÓN SINTÁCTICA EN SANDBOX ---")
    try:
        subprocess.run(["docker", "build", "-t", "iot-sandbox", "."], check=True, capture_output=True)
        
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{os.getcwd()}:/app", "iot-sandbox", "python", "-m", "py_compile", "patch_test.py"],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print("VALIDACIÓN SINTÁCTICA EXITOSA: El parche es código Python válido.")
            return True
        else:
            print(f"ERROR DE SINTAXIS EN EL PARCHE:\n{result.stderr}")
            return False
    except Exception as e:
        print(f"ERROR TÉCNICO: {e}")
        return False