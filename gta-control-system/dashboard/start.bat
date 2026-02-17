@echo off
title GTA V Dashboard - PILLAR V7
color 0A

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   🎮 GTA V DASHBOARD PILLAR V7                        ║
echo ║   Iniciando servidor...                               ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Verificar si Node.js está instalado
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ ERROR: Node.js no está instalado
    echo.
    echo Por favor instala Node.js desde: https://nodejs.org
    pause
    exit /b 1
)

REM Verificar si las dependencias están instaladas
if not exist "node_modules\" (
    echo 📦 Instalando dependencias...
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ ERROR: Falló la instalación de dependencias
        pause
        exit /b 1
    )
)

REM Iniciar el servidor
echo ✅ Iniciando dashboard...
echo.
echo 🌐 Abre tu navegador en: http://localhost:3000
echo.
echo ⚠️  Para detener el servidor, presiona Ctrl+C
echo.

node app.js

pause
