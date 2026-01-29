@echo off
echo ========================================
echo RAG Chatbot - Quick Start
echo ========================================
echo.

echo Step 1: Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing backend dependencies...
pip install -r requirements.txt

echo.
echo Step 2: Setting up Frontend...
cd ..\frontend

echo Installing frontend dependencies...
call npm install

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo IMPORTANT: Edit .env file and add your OPENAI_API_KEY
echo.
echo To start the application:
echo   1. Backend:  cd backend ^&^& python main.py
echo   2. Frontend: cd frontend ^&^& npm run dev
echo.
echo Press any key to exit...
pause > nul
