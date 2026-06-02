import os
import subprocess
import pickle
import base64

def process_gateway_request(user_input):
    """
    Este archivo es un test de nivel avanzado para el TFM.
    Contiene dos fallos críticos que Bandit SIEMPRE detecta:
    1. CWE-78: Command Injection via shell=True
    2. CWE-502: Insecure Deserialization (Pickle)
    """
    
    print(f"Procesando comando de pasarela: {user_input}")
    
    # TEST 1: Inyección de comandos crítica
    # Bandit detecta esto como B602 (subprocess_popen_with_shell_equals_true)
    # Es difícil porque el parche debe eliminar shell=True y convertir a lista
    subprocess.call("echo 'Log entry: ' + user_input", shell=True)

    # TEST 2: Deserialización insegura
    # Bandit detecta esto como B301 (pickle)
    # Es difícil porque el parche debe proponer una alternativa segura (como JSON)
    if user_input.startswith("data:"):
        raw_data = user_input.split(":")[1]
        decoded_data = base64.b64decode(raw_data)
        # FALLO CRÍTICO: Ejecución de código arbitrario al cargar el objeto
        config_obj = pickle.loads(decoded_data)
        return config_obj

    return "Request processed"

if __name__ == "__main__":
    # Ejemplo de uso peligroso
    process_gateway_request("admin; rm -rf /")