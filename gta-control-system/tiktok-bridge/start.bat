@echo off
title TikTok Live Bridge - GTA V
color 0A

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   🎮 TikTok Live Bridge - GTA V                       ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Verificar que Node.js esté instalado
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js no está instalado
    echo.
    echo 💡 Descarga Node.js desde: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

REM Verificar que las dependencias estén instaladas
if not exist "node_modules\" (
    echo 📦 Instalando dependencias...
    echo.
    call npm install
    echo.
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Error instalando dependencias
        pause
        exit /b 1
    )
)

REM Solicitar nombre de usuario de TikTok
echo.
set /p TIKTOK_USER="📺 Ingresa tu nombre de usuario de TikTok: "

if "%TIKTOK_USER%"=="" (
    echo ❌ Debes ingresar un nombre de usuario
    pause
    exit /b 1
)

echo.
echo ✅ Iniciando bridge con usuario: %TIKTOK_USER%
echo.
echo 💡 Presiona Ctrl+C para detener
echo.
echo ════════════════════════════════════════════════════════
echo.

REM Iniciar el listener
node tiktok_listener.js %TIKTOK_USER%

pause
