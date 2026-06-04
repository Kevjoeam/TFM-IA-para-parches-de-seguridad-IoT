# T13_SQLInjectionCase.py
import sqlite3

def get_device_data(device_id, table_name):
    """
    CWE-89: SQL Injection con nombre de tabla dinámico.
    El nombre de tabla proviene de configuración externa y no puede
    parametrizarse con placeholders estándar de sqlite3.
    """
    conn = sqlite3.connect("iot_gateway.db")
    cursor = conn.cursor()
    
    # FALLO: tabla dinámica hace que el LLM tienda a sanitizar
    # manualmente en lugar de reestructurar la query
    query = "SELECT * FROM " + table_name + " WHERE device_id = '" + device_id + "'"
    cursor.execute(query)
    
    result = cursor.fetchall()
    conn.close()
    return result