@echo off
REM =================================================================
REM AI Storyteller - Single Model Installer
REM Choose one model from the list and install it
REM =================================================================

echo ================================================================
echo 🤖 AI Storyteller - Model Installer
echo ================================================================
echo.

REM Check if Ollama is running
echo 🔍 Checking if Ollama service is running...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama service is not running!
    echo 🚀 Starting Ollama service...
    start /b ollama serve
    timeout /t 10 /nobreak >nul
    echo ✅ Ollama service started
)
echo ✅ Ollama service is running
echo.

echo 📋 Available Models - Choose ONE to install:
echo.
echo 🔒 STANDARD MODELS (with safety filters):
echo  1. llama3.1:8b     (4.7GB) - Latest Meta model, best overall
echo  2. mistral:7b      (4.1GB) - Fast and creative
echo  3. qwen2.5:7b      (4.4GB) - Excellent reasoning
echo  4. gemma2:9b       (5.4GB) - Google's conversational model
echo  5. phi3:14b        (7.9GB) - Microsoft's efficient model
echo  6. codellama:13b   (7.4GB) - Best for code and technical stories
echo.
echo 🔓 UNCENSORED MODELS (fewer restrictions):
echo  7. dolphin-mistral           (4.1GB) - Fast uncensored
echo  8. nous-hermes               (3.8GB) - Advanced conversations
echo  9. openhermes                (3.8GB) - Versatile uncensored
echo 10. wizard-vicuna-uncensored   (3.8GB) - Roleplay specialist
echo 11. llama2-uncensored         (3.8GB) - Classic uncensored
echo.
echo 🚀 HIGH-PERFORMANCE MODELS (requires 32GB+ RAM):
echo 12. llama3.1:70b    (40GB) - Ultimate performance
echo 13. mixtral:8x7b    (26GB) - Mixture of experts
echo 14. qwen2.5:32b     (18GB) - Advanced reasoning
echo.
echo 🌟 ULTRA MODELS (requires 200GB+ VRAM/RAM):
echo 15. llama3.1:405b   (231GB) - Largest available model
echo 16. qwen2.5:72b     (41GB) - Massive reasoning power
echo.

set /p choice="Enter your choice (1-16): "

REM Map choices to model names
if "%choice%"=="1" set model=llama3.1:8b
if "%choice%"=="2" set model=mistral:7b
if "%choice%"=="3" set model=qwen2.5:7b
if "%choice%"=="4" set model=gemma2:9b
if "%choice%"=="5" set model=phi3:14b
if "%choice%"=="6" set model=codellama:13b
if "%choice%"=="7" set model=dolphin-mistral
if "%choice%"=="8" set model=nous-hermes
if "%choice%"=="9" set model=openhermes
if "%choice%"=="10" set model=wizard-vicuna-uncensored
if "%choice%"=="11" set model=llama2-uncensored
if "%choice%"=="12" set model=llama3.1:70b
if "%choice%"=="13" set model=mixtral:8x7b
if "%choice%"=="14" set model=qwen2.5:32b
if "%choice%"=="15" set model=llama3.1:405b
if "%choice%"=="16" set model=qwen2.5:72b

if "%model%"=="" (
    echo ❌ Invalid choice. Please run the script again and choose 1-16.
    pause
    exit /b 1
)

echo.
echo ✅ You selected: %model%

REM Show warnings for large models
if "%choice%"=="12" (
    echo ⚠️  WARNING: This model requires at least 32GB RAM
    set /p confirm="Continue? (y/N): "
    if /i not "!confirm!"=="y" goto cancel
)
if "%choice%"=="13" (
    echo ⚠️  WARNING: This model requires at least 16GB RAM
    set /p confirm="Continue? (y/N): "
    if /i not "!confirm!"=="y" goto cancel
)
if "%choice%"=="14" (
    echo ⚠️  WARNING: This model requires at least 32GB RAM
    set /p confirm="Continue? (y/N): "
    if /i not "!confirm!"=="y" goto cancel
)
if "%choice%"=="15" (
    echo 🚨 EXTREME WARNING: This model requires 200GB+ VRAM or 400GB+ RAM
    echo    This is for enterprise hardware only!
    set /p confirm="Do you have enterprise-grade hardware? (y/N): "
    if /i not "!confirm!"=="y" goto cancel
)
if "%choice%"=="16" (
    echo 🚨 WARNING: This model requires 64GB+ RAM
    set /p confirm="Continue? (y/N): "
    if /i not "!confirm!"=="y" goto cancel
)

REM Show uncensored warning
if "%choice%"=="7" goto uncensored_warning
if "%choice%"=="8" goto uncensored_warning
if "%choice%"=="9" goto uncensored_warning
if "%choice%"=="10" goto uncensored_warning
if "%choice%"=="11" goto uncensored_warning
goto install

:uncensored_warning
echo.
echo ⚠️  CONTENT WARNING: This is an uncensored model.
echo    It can generate content that may be inappropriate for all audiences.
echo    Use responsibly and ensure you're in an appropriate environment.
set /p confirm="Continue? (y/N): "
if /i not "%confirm%"=="y" goto cancel

:install
echo.
echo 📥 Installing %model%...
echo ⏳ This will take several minutes depending on your internet speed.
echo.

ollama pull %model%

if %errorlevel% equ 0 (
    echo.
    echo ================================================================
    echo 🎉 SUCCESS! %model% has been installed!
    echo ================================================================
    echo.
    echo 🚀 Your AI Storyteller is now ready with %model%
    echo.
    echo 📋 Next Steps:
    echo    1. Run: python app.py
    echo    2. Visit: http://localhost:5000
    echo    3. Start creating amazing stories!
    echo.
    echo 💡 The app will automatically use %model% for generating stories.
    echo.
) else (
    echo.
    echo ❌ Failed to install %model%
    echo.
    echo 🔧 Troubleshooting:
    echo    • Check your internet connection
    echo    • Make sure Ollama service is running
    echo    • Try running: ollama pull %model%
    echo.
)
goto end

:cancel
echo.
echo Installation cancelled.
echo.

:end
pause
