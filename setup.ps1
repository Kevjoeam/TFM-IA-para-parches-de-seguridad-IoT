# Script de configuración inicial para el TFM - Automatización de Parches IoT
# Alumno: Kevin Joel Ammirata

Write-Host "------------------------------------------------------------" -ForegroundColor Cyan
Write-Host "CONFIGURACIÓN DEL PLANO DE CONTROL (NIVEL 3)" -ForegroundColor Cyan
Write-Host "------------------------------------------------------------" -ForegroundColor Cyan

# 1. Comprobar versión de Python
$pythonVersion = python --version 2>&1
if ($lastExitCode -ne 0) {
    Write-Host "Error: Python no está instalado o no está en el PATH." -ForegroundColor Red
    exit
}
Write-Host "Python detectado: $pythonVersion"

# 2. Comprobar Docker (Necesario para el Sandbox de Validación RF6)
Write-Host "Comprobando Docker Desktop" -ForegroundColor Yellow
docker ps > $null 2>&1
if ($lastExitCode -ne 0) {
    Write-Host "Docker no parece estar corriendo. El Sandbox no funcionará sin Docker." -ForegroundColor Magenta
} else {
    Write-Host "Docker está activo." -ForegroundColor Green
}

# 3. Comprobar Ollama (Necesario para la inferencia con Llama-3)
Write-Host "Comprobando servicio de IA (Ollama)" -ForegroundColor Yellow
curl.exe -s http://localhost:11434/api/tags > $null
if ($lastExitCode -ne 0) {
    Write-Host "Ollama no detectado. Asegúrate de que Ollama esté abierto" -ForegroundColor Magenta
} else {
    Write-Host "Ollama está activo." -ForegroundColor Green
}

# 4. Crear Entorno Virtual (.venv)
if (!(Test-Path ".venv")) {
    Write-Host "Creando entorno virtual de Python" -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "Entorno virtual creado." -ForegroundColor Green
} else {
    Write-Host "El entorno virtual ya existe." -ForegroundColor Gray
}

# 5. Crear Estructura de Carpetas de Datos y Uploads
$reportPath = "data/reports"
$uploadPath = "uploads"

if (!(Test-Path $reportPath)) {
    Write-Host "Creando estructura de directorios: $reportPath" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $reportPath -Force | Out-Null
}
if (!(Test-Path $uploadPath)) {
    Write-Host "Creando carpeta de uploads para el usuario: $uploadPath" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $uploadPath -Force | Out-Null
}
Write-Host "Carpetas de sistema configuradas." -ForegroundColor Green

# 6. Instalar Dependencias
if (Test-Path "requirements.txt") {
    Write-Host "Instalando dependencias desde requirements.txt" -ForegroundColor Yellow
    & .venv\Scripts\python.exe -m pip install --upgrade pip | Out-Null
    & .venv\Scripts\pip install -r requirements.txt
    if ($lastExitCode -eq 0) {
        Write-Host "Todas las librerías se instalaron correctamente." -ForegroundColor Green
    } else {
        Write-Host "Hubo un problema instalando las dependencias." -ForegroundColor Red
    }
} else {
    Write-Host "Error: No se encuentra el archivo requirements.txt." -ForegroundColor Red
}

Write-Host "------------------------------------------------------------" -ForegroundColor Cyan
Write-Host "¡TODO LISTO!" -ForegroundColor Green
Write-Host "Para lanzar el dashboard usa: .\run_app.bat" -ForegroundColor White
Write-Host "------------------------------------------------------------" -ForegroundColor Cyan