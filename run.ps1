# Inicia EstaticaBot creando el entorno virtual si hace falta.
# Uso:  .\run.ps1

$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
$venvStreamlit = Join-Path $PSScriptRoot ".venv\Scripts\streamlit.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "Creando entorno virtual .venv ..." -ForegroundColor Cyan
    py -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        throw "No se pudo crear el entorno virtual. Verifica que Python 3.10+ este instalado."
    }
}

if (-not (Test-Path $venvStreamlit)) {
    Write-Host "Instalando dependencias ..." -ForegroundColor Cyan
    & $venvPython -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) { throw "Fallo la actualizacion de pip." }
    & $venvPython -m pip install -r (Join-Path $PSScriptRoot "requirements.txt")
    if ($LASTEXITCODE -ne 0) { throw "Fallo la instalacion de dependencias." }
}

Write-Host "Iniciando EstaticaBot en http://localhost:8501 ..." -ForegroundColor Green
& $venvPython -m streamlit run (Join-Path $PSScriptRoot "app.py")
