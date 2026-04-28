#!/bin/bash
# NutriCoach AI - Unified Starter (Unix/Mac/Linux)
# Single command to build frontend and start backend

clear
echo ""
echo "============================================================"
echo "  🥗 NutriCoach AI - Unified Startup"
echo "============================================================"
echo ""

echo "[1/4] Installing dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "⚠ WARNING: npm install had issues"
fi

echo ""
echo "[2/4] Building Frontend..."
npm run build
if [ $? -ne 0 ]; then
    echo "⚠ WARNING: Frontend build failed"
fi

echo ""
echo "[3/4] Initializing Database..."
python3 backend/init_db.py
if [ $? -ne 0 ]; then
    echo "⚠ WARNING: Database initialization had issues"
fi

echo ""
echo "[4/4] Seeding Recipes..."
python3 backend/seed_recipes.py
if [ $? -ne 0 ]; then
    echo "⚠ WARNING: Recipe seeding had issues"
fi

echo ""
echo "============================================================"
echo "  SUCCESS! Starting NutriCoach..."
echo "============================================================"
echo ""
echo "  🌐 http://localhost:5000"
echo "  ⏹ Press Ctrl+C to stop"
echo ""

python3 backend/wsgi.py
