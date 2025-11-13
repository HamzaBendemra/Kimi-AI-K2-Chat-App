@echo off
echo Starting Kimi AI Chat Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install -r requirements.txt
)

REM Run the Streamlit app
echo.
echo 🚀 Starting Kimi AI Chat App...
echo 📝 Make sure to enter your API key in the sidebar
echo.
streamlit run kimi_chat_app.py

pause