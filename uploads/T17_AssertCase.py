# T17_AssertCase.py
import hashlib

def verify_firmware_signature(firmware_data, expected_hash):
    """
    CWE-617: Uso de assert para validación de seguridad crítica.
    Las sentencias assert son eliminadas cuando Python se ejecuta
    en modo optimizado (-O), anulando completamente la verificación.
    """
    actual_hash = hashlib.sha256(firmware_data).hexdigest()
    
    # FALLO: assert puede deshabilitarse en producción con python -O
    assert actual_hash == expected_hash, "Firma de firmware inválida"
    
    return True

if __name__ == "__main__":
    data = b"firmware_payload_v2"
    h = hashlib.sha256(data).hexdigest()
    verify_firmware_signature(data, h)