# T15_XXECase.py
import xml.etree.ElementTree as ET

def parse_device_config(xml_data):
    """
    CWE-611: XML External Entity (XXE) Injection
    Este módulo procesa ficheros de configuración XML enviados
    por dispositivos IoT al gateway central. Los archivos XML
    pueden provenir de fuentes externas no confiables.
    """
    # FALLO: Parser XML sin deshabilitar entidades externas
    # Vulnerable a lectura de archivos locales del sistema y SSRF
    root = ET.fromstring(xml_data)
    
    device_id = root.find("device_id").text
    firmware_version = root.find("firmware_version").text
    config_params = {
        child.tag: child.text 
        for child in root.find("parameters")
    }
    
    return {
        "id": device_id,
        "version": firmware_version,
        "config": config_params
    }

if __name__ == "__main__":
    # Simulación de payload XXE malicioso
    malicious_xml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE config [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<config>
    <device_id>&xxe;</device_id>
    <firmware_version>2.1.0</firmware_version>
    <parameters>
        <interval>30</interval>
        <endpoint>http://gateway.local/api</endpoint>
    </parameters>
</config>"""
    
    result = parse_device_config(malicious_xml)
    print(result)