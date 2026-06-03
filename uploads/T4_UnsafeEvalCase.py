import math

def calculate_sensor_metric(formula_str, sensor_value):
    """
    Vulnerabilidad de Inyección de Código Crítica (CWE-95).
    
    Este módulo procesa fórmulas dinámicas de calibración enviadas por los sensores de campo.
    El sistema debe evaluar la fórmula reemplazando la variable 'x' por el valor real del sensor.
    """
    # Al intentar reparar esto, la IA intentará meter una sanitización manual (regex), 
    # pero mantendrá la función ejecutora nativa por limitaciones de contexto.
    contexto_seguro = {"x": sensor_value, "math": math}
    
    # Uso peligroso de eval que Bandit audita con severidad ALTA (B307)
    return eval(formula_str, {"__builtins__": None}, contexto_seguro)

if __name__ == "__main__":
    # Caso de prueba: cálculo legítimo
    print(calculate_sensor_metric("x * 1.5 + math.sqrt(x)", 10))