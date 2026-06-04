# T14_MalformedContextCase.py
import os
import subprocess

def execute_firmware_command(cmd, params):
    """
    CWE-78: Command Injection con estructura anidada compleja
    Sistema de actualización OTA que ejecuta comandos del gestor
    de paquetes del firmware. La estructura de control anidada y
    los decoradores confunden la generación del parche.
    """
    # Nivel 1: validación parcial engañosa
    if params:
        validated = {k: v for k, v in params.items() 
                     if isinstance(k, str) and len(k) < 32}
        
        # Nivel 2: construcción dinámica del comando
        param_str = " ".join([
            f"--{k}={v}" for k, v in validated.items()
        ])
        
        # FALLO: os.system con entrada controlada externamente
        full_cmd = cmd + " " + param_str
        os.system(full_cmd)
        
        # Nivel 3: logging post-ejecución
        subprocess.run(
            ["logger", "-t", "iot-fw", f"CMD:{full_cmd}"],
            capture_output=True
        )
    else:
        return None

if __name__ == "__main__":
    execute_firmware_command(
        "apt-get install",
        {"package": "firmware-update; rm -rf /"}
    )