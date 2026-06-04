@echo off
title Ejecutar Dashboard
echo Iniciando Dashboard de Parche IoT...
echo ---------------------------------------
:: Activar entorno virtual si existe
if exist .venv\Scripts\activate (
    call .venv\Scripts\activate
)
:: Lanzar Streamlit
python -m streamlit run src/dashboard/app.py
pause