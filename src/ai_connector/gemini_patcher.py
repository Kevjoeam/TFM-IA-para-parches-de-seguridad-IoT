from google import genai
import os
import sys

# 1. Configuración de la API (Sustituye por tu clave o usa una variable de entorno)
API_KEY = "AIzaSyClDXPvmqxYfiWCt0_LRpUBugU4o4mxYJk"
client = genai.Client(api_key=API_KEY)

def generate_iot_patch(vulnerable_code, vulnerability_desc):
    """
    Genera un parche de seguridad usando el SDK moderno (RF3 y RF4).
    """
    # En 2026 usamos gemini-2.0-flash o el modelo estable actual
    model_id = "gemini-2.0-flash" 
    
    prompt = f"""
    Actúa como experto en ciberseguridad IoT.
    Vulnerabilidad detectada: {vulnerability_desc}
    
    Código original vulnerable:
    ```python
    {vulnerable_code}
    ```
    
    Instrucciones de remediación:
    1. Analiza el fallo (CWE-78).
    2. Reescribe la función usando 'subprocess.run' con una lista de argumentos (sin shell=True).
    3. Devuelve únicamente el bloque de código corregido, sin explicaciones adicionales.
    """
    
    try:
        # Nueva sintaxis del SDK 2026
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error crítico en la inferencia: {e}"

if __name__ == "__main__":
    # Aseguramos que Python encuentre el podador de AST (RF2)
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from ast_engine.context_pruner import prune_vulnerable_context
    
    report_path = "data/reports/vulnerability_report.json"
    contexto, issue = prune_vulnerable_context(report_path)
    
    if contexto:
        print("\n--- ENVIANDO A LA IA PARA GENERACIÓN DE PARCHE ---")
        patch = generate_iot_patch(contexto, issue['issue_text'])
        print("\n--- PROPUESTA DE PARCHE (SELF-HEALING) ---")
        print(patch)   # Importamos el podador para obtener los datos reales
    # Agregamos la ruta para que Python encuentre el módulo
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from ast_engine.context_pruner import prune_vulnerable_context
    
    report_path = "data/reports/vulnerability_report.json"
    contexto, issue = prune_vulnerable_context(report_path)
    
    if contexto:
        print("\n--- ENVIANDO A GEMINI PARA PARCHEO ---")
        patch = generate_iot_patch(contexto, issue['issue_text'])
        print("\n--- PROPUESTA DE PARCHE GENERADA ---")
        print(patch)