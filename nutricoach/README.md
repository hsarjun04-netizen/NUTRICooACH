# NutriCoach - AI-Powered Nutrition Coaching

A full-stack monorepo project with Vue.js frontend and Python Flask backend.

## Project Structure

```
nutricoach/
├── frontend/              # Vue 3 + Vite web application
│   ├── src/              # Vue components, pages, stores
│   ├── package.json      # Frontend dependencies
│   ├── vite.config.js    # Vite configuration
│   └── dist/             # Built frontend (generated)
├── backend/              # Python Flask API
│   ├── app.py           # Main Flask app
│   ├── requirements.txt  # Python dependencies
│   ├── wsgi.py          # WSGI entry point
│   └── database.db      # SQLite database
├── package.json         # Root monorepo configuration
├── render.yaml          # Deployment configuration
└── README.md           # This file
```

## Getting Started

### Prerequisites
- Node.js 20.11.0+
- Python 3.11.0+
- npm

### Installation

```bash
# Install all dependencies (frontend + root tools)
npm install
```

### Development

**Frontend only:**
```bash
npm run dev
```

**Backend only:**
```bash
cd backend
python wsgi.py
```

**Both together:**
- Terminal 1: `npm run dev` (frontend starts on http://localhost:5173)
- Terminal 2: `cd backend && python wsgi.py` (backend starts on http://localhost:5000)

### Building

**Frontend:**
```bash
npm run build
```

**Preview built frontend:**
```bash
npm run preview
```

## Features

- **Frontend**: Vue 3 with Vite, Vue Router, Pinia state management, Chart.js visualizations
- **Backend**: Python Flask API with JWT authentication, SQLite database
- **Database**: Meal recipes, user nutritional tracking, personalized recommendations
- **Deployment**: Render.com with Python + Node.js runtime
- User registration and authentication
- Dietary preferences and restriction tracking
- Personalized meal plan generation
- Progress tracking and charts
- Mobile-responsive design

## Tech Stack

- Frontend: Vue 3, Vite
- Backend: Python, Flask
- Database: SQLite
- Deployment: Render.com

## Available Scripts

### Root Level
- `npm run dev` - Start frontend dev server
- `npm run build` - Build frontend for production
- `npm run preview` - Preview production build
- `npm run install-all` - Install all dependencies
- `npm run clean` - Clean all generated files

### Backend
```bash
cd backend
python init_db.py      # Initialize database
python seed_recipes.py # Seed recipe data
python wsgi.py         # Start Flask server
```

## API Documentation

See `backend/API.md` for complete API documentation.

## Deployment

The project is configured for deployment on Render.com via `render.yaml`:

```yaml
buildCommand: |
  pip install -r backend/requirements.txt
  python backend/init_db.py
  python backend/seed_recipes.py
  npm install
  npm run build
```

## Development Notes

- Frontend is served from `frontend/dist/` after build
- Backend serves both API and static frontend assets
- Environment variables are managed in `render.yaml`
- Database uses SQLite for simplicity (can be upgraded to PostgreSQL for production)

## License

MIT