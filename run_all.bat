@echo off
setlocal

:: -------------------------------------------------
:: 1️⃣  Ensure a Python virtual‑env exists
:: -------------------------------------------------
if not exist ".venv" (
    echo Creating virtual environment...\r
    python -m venv .venv
)

:: -------------------------------------------------
:: 2️⃣  Activate the venv and start the Flask backend
:: -------------------------------------------------
start "Backend" cmd /k "cd /d %~dp0 && .\.venv\Scripts\activate && python app.py"

:: -------------------------------------------------
:: 3️⃣  Start the Vue frontend dev server
:: -------------------------------------------------
start "Frontend" cmd /k "cd /d %~dp0frontend && npm install && npm run dev"

echo.
echo =================================================
echo  Nutri‑Coach is now running:
echo   • Backend API : http://127.0.0.1:5000/api/v1/
echo   • Front‑end UI: http://localhost:5173/
echo  Close the two terminal windows to stop the app.
echo =================================================
pause
