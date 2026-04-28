@echo off
REM NutriCoach AI - Unified Starter (Windows)
REM Single command to build frontend and start backend

cls
echo.
echo ============================================================
echo  ^|^|^| NutriCoach AI - Unified Startup ^^^|^^^|^^^|
echo ============================================================
echo.

echo [1/4] Installing dependencies...
call npm install
if errorlevel 1 (
    echo WARNING: npm install had issues
)

echo.
echo [2/4] Building Frontend...
call npm run build
if errorlevel 1 (
    echo WARNING: Frontend build failed
)

echo.
echo [3/4] Initializing Database...
python backend\init_db.py
if errorlevel 1 (
    echo WARNING: Database initialization had issues
)

echo.
echo [4/4] Seeding Recipes...
python backend\seed_recipes.py
if errorlevel 1 (
    echo WARNING: Recipe seeding had issues
)

echo.
echo ============================================================
echo  SUCCESS! Starting NutriCoach...
echo ============================================================
echo.
echo  ^|^| http://localhost:5000
echo  ^|^| Press Ctrl+C to stop
echo.

python backend\wsgi.py

pause
