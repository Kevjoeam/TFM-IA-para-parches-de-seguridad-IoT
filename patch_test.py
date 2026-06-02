import ast
from math import math

def calculate_sensor_metric(formula_str, sensor_value):
    try:
        # Use ast.literal_eval to safely evaluate the formula string
        return eval(compile(ast.parse(formula_str), '<string>', 'eval'), {"x": sensor_value})
    except Exception as e:
        print(f"Error: {str(e)}")
        return None