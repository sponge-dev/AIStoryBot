@echo off
echo ========================================
echo    AI Storyteller - Quick Start
echo ========================================
echo.

echo Checking if Ollama is installed...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ollama not found. Running setup...
    python setup_ollama.py
    if %errorlevel% neq 0 (
        echo Setup failed. Please run setup_ollama.py manually.
        pause
        exit /b 1
    )
) else (
    echo Ollama is installed.
)

echo.
echo Starting AI Storyteller...
echo.
echo The web interface will open at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause 