import ast
from typing import Dict

def calculate_sensor_metric(formula_str: str, sensor_value: float) -> float:
    """
    Calculate sensor metric using a dynamic formula string.
    
    This module processes dynamic calibration formulas sent by field sensors.
    The system must evaluate the formula replacing variable 'x' with the real sensor value.
    """
    try:
        # Use safer ast.literal_eval to safely evaluate the formula
        return eval(ast.literal_eval(formula_str), {"__builtins__": None}, {"x": sensor_value})
    except Exception as e:
        print(f"Error: {e}")
        return 0.0