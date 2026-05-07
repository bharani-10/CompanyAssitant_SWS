@echo off
REM Setup script for Windows

echo.
echo ============================================
echo SWS AI Company Assistant Chatbot - Setup
echo ============================================
echo.

REM Step 1: Create virtual environment
echo [1/5] Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error creating virtual environment
    exit /b 1
)

REM Step 2: Activate virtual environment
echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

REM Step 3: Install dependencies
echo [3/5] Installing dependencies...
pip install -r requirements.txt --upgrade
if errorlevel 1 (
    echo Error installing dependencies
    exit /b 1
)

REM Step 4: Create .env file if not exists
echo [4/5] Setting up environment configuration...
if not exist .env (
    copy .env.example .env
    echo.
    echo ⚠️  Created .env file - PLEASE EDIT IT!
    echo Add your OPENAI_API_KEY to .env
    echo.
    pause
)

REM Step 5: Initialize vector store
echo [5/5] Initializing vector store from PDFs...
python -c "from document_ingestion import initialize_pipeline; initialize_pipeline('.', rebuild=True)"

echo.
echo ============================================
echo ✅ Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Edit .env and add your OPENAI_API_KEY
echo 2. In Terminal 1: python main.py
echo 3. In Terminal 2: streamlit run app.py
echo 4. Open http://localhost:8501
echo.
pause
