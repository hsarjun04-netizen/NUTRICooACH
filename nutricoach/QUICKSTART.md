# 🥗 NutriCoach AI - Quick Start Guide

## Single Command Execution

### **Windows Users** 🪟
Simply double-click or run:
```bash
start.bat
```

Or from terminal:
```bash
npm run start
```

### **Mac/Linux Users** 🍎🐧
Make script executable first:
```bash
chmod +x start.sh
./start.sh
```

Or use npm:
```bash
npm run start:unified
```

---

## What This Does (Automatically)
1. ✅ Installs all dependencies (Node + Python)
2. ✅ Builds Vue frontend
3. ✅ Initializes SQLite database
4. ✅ Seeds recipe data
5. ✅ Starts Flask backend server

**Result:** Full app running at **http://localhost:5000** 🚀

---

## Project Structure (Merged)
```
nutricoach/
├── backend/          ← Python Flask API
│   ├── app.py       ← Main server (serves frontend + API)
│   ├── wsgi.py      ← Production entry point
│   ├── requirements.txt
│   └── database.db
│
├── frontend/         ← Vue 3 source (built to dist/)
│   ├── src/
│   ├── dist/        ← Built files served by Flask
│   └── package.json
│
├── start.bat        ← Windows auto-runner ⭐
├── start.sh         ← Unix/Mac auto-runner ⭐
├── start.py         ← Python runner
├── package.json     ← Root config
└── README.md
```

---

## Available Commands

| Command | Purpose |
|---------|---------|
| `npm run start` | Build frontend + start backend (single command) |
| `npm run setup` | Setup everything from scratch |
| `npm run build` | Build frontend only |
| `npm run dev` | Frontend dev server (http://localhost:5173) |
| `npm run backend` | Start backend only |
| `npm run db:init` | Initialize database |
| `npm run db:seed` | Seed recipes |
| `npm run clean` | Remove all generated files |

---

## Troubleshooting

**Port 5000 already in use?**
```bash
# Change port in environment
set PORT=5001
npm run start
```

**Frontend not loading?**
1. Check build succeeded: `npm run build`
2. Check frontend/dist exists
3. Restart backend

**Database issues?**
```bash
# Reset database
rm backend/database.db
npm run db:init
npm run db:seed
```

---

## Development Workflow

### For Frontend Development:
```bash
# Terminal 1: Start dev server
npm run dev

# Terminal 2: Start backend
npm run backend
```
- Frontend rebuilds automatically on file changes
- API available at http://localhost:5000/api/v1/

### For Backend Development:
```bash
# Terminal 1: Start backend with auto-reload
cd backend
pip install flask-cors
python wsgi.py

# Terminal 2: Build frontend when needed
npm run build
```

---

## Production Deployment

The app is configured for **Render.com**:
- Build command: Installs deps + builds frontend
- Start command: Runs `python backend/wsgi.py`
- Serves both API and static frontend from single process

See `render.yaml` for details.

---

**Happy coding! 🚀**
