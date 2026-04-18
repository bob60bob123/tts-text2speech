@echo off
chcp 65001 >nul 2>&1
title TTS Service
echo ========================================
echo        Text-to-Speech TTS Launcher
echo ========================================
echo.

cd /d "%~dp0"

echo [CHECK] Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)
echo [OK] Python detected

echo.
echo [CHECK] Dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Installing dependencies...
    pip install -r requirements.txt
)
echo [OK] Dependencies ready

echo.
echo [CHECK] Code syntax...
python -m py_compile app/main.py app/api/routes.py app/services/tts_service.py 2>nul
if errorlevel 1 (
    echo [ERROR] Syntax check failed!
    pause
    exit /b 1
)
echo [OK] Syntax OK

echo.
echo [CLEAN] Stop old service...
taskkill /F /IM uvicorn.exe >nul 2>&1

echo.
echo ========================================
echo   Starting service...
echo ========================================
echo.
echo URL: http://127.0.0.1:8000/
echo.

start /b python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

timeout /t 2 /nobreak >nul

curl -s http://127.0.0.1:8000/api/health >nul 2>&1
if not errorlevel 1 (
    echo [OK] Service started successfully!
    start http://127.0.0.1:8000
) else (
    echo [WARN] Please check if service started
)

echo.
pause
