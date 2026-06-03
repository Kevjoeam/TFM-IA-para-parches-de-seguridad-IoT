# Automatización de Parches IoT

TFM de Ciberseguridad — Universitat Oberta de Catalunya  
Alumno: Kevin Joel Ammirata

Sistema de reparación de vulnerabilidades en entornos IoT 
mediante análisis estático (Bandit), poda de contexto (AST) 
e inferencia local con LLM (Llama-3).

## Requisitos previos

- [Python 3.11+](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Ollama](https://ollama.ai)*

*El modelo llama3 pesa ~4GB. La descarga inicial puede tardar varios minutos.

## Instalación (Windows)

1. Clona el repositorio
   git clone https://github.com/Kevjoeam/TFM-IA-para-parches-de-seguridad-IoT
   cd TFM-IA-para-parches-de-seguridad-IoT

2. Ejecuta el setup (crea entorno virtual e instala dependencias)
   ./setup.ps1

3. Descarga el modelo IA
   ollama pull llama3

4. Inicia Docker Desktop y espera a que esté corriendo

5. Lanza el dashboard
   ./run_app.bat

6. Si no inicia automáticamente, abre el navegador en http://localhost:8501


## Instalación (Linux / macOS)

1. Clona el repositorio
   git clone https://github.com/Kevjoeam/TFM-IA-para-parches-de-seguridad-IoT
   cd TFM-IA-para-parches-de-seguridad-IoT

2. Crea el entorno virtual
   python3 -m venv .venv
   source .venv/bin/activate

3. Instala dependencias
   pip install -r requirements.txt

4. Descarga el modelo IA
   ollama pull llama3

5. Inicia Docker
   sudo systemctl start docker  

6. Ejecuta el dashboard
   streamlit run src/dashboard/app.py

7. Abre el navegador en http://localhost:8501

## Uso

1. Sube un archivo .py con código vulnerable (o selecciona uno de los ejemplos en /src)
2. Pulsa ESCANEAR
3. El sistema detectará vulnerabilidades, generará un parche y lo validará 
4. Revisa el resultado en el panel de auditoría

## Casos de prueba incluidos

| Archivo | Vulnerabilidad | CWE |
|---------|---------------|-----|
| T1_CommandInjection.py | Inyección de comando | CWE-78 |
| T2_AdvancedFirmware.py | Command Injection + Deserialización | CWE-78 / CWE-502 |
| T3_WeakCrypto.py | Hash inseguro MD5 | CWE-327 |
| T4_UnsafeEvalCase.py | Inyección de código eval() | CWE-95 |
| T5_ControlCase.py | Sin vulnerabilidades | — |

## Tecnologías utilizadas

- Bandit — Análisis estático SAST
- Llama-3 (Ollama) — Generación local de parches
- Docker — Sandbox de validación aislada
- Streamlit — Dashboard de visualización
- Python AST — Poda de contexto

## Repositorio

https://github.com/Kevjoeam/TFM-IA-para-parches-de-seguridad-IoT
