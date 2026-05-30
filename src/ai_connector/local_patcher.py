import ollama

MODEL_NAME = "llama3"

def generate_local_patch(vulnerable_code, vulnerability_desc):
    """
    Genera un parche genérico basado en la descripción de la vulnerabilidad (RF3/RF4).
    """
    # Prompt Universal (Chain-of-Thought)
    prompt = f"""
    [ROLE] Act as an expert IoT Security Engineer.
    [CONTEXT] You are part of a self-healing system for critical infrastructures[cite: 32].
    
    [VULNERABILITY DETECTED]
    Description: {vulnerability_desc}
    
    [CODE TO REPAIR]
    ```python
    {vulnerable_code}
    ```
    
    [INSTRUCTIONS]
    1. Identify the root cause based on the description.
    2. Rewrite the function using secure coding standards (OWASP IoT Top 10)[cite: 484].
    3. If it's a command injection, use 'subprocess' with lists.
    4. If it's hardcoded credentials, implement a configuration-based approach.
    5. RETURN ONLY THE CORRECTED CODE. No explanations.
    """
    
    try:
        response = ollama.chat(model=MODEL_NAME, messages=[
            {'role': 'user', 'content': prompt},
        ])
        return response['message']['content']
    except Exception as e:
        return f"Error en inferencia local: {e}"