# NutriCoach AI

A personalized diet plan generator web application built with Vue.js frontend and Python backend.

## Features
- User registration and authentication
- Dietary preferences and restriction tracking
- Personalized meal plan generation
- Progress tracking and charts
- Mobile-responsive design

## Tech Stack
- Frontend: Vue.js
- Backend: Python (Flask)
- Database: SQLite (via SQLAlchemy)
- Deployment: Docker

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.11+)
- Docker (optional for deployment)

### Running the Application

#### Frontend
```bash
cd nutricoach/frontend
npm install
npm run dev
```

#### Backend
```bash
cd nutricoach/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Database Setup
```bash
cd nutricoach/backend
python init_db.py
```

## API Endpoints
See [API Documentation](backend/API.md) for detailed endpoint descriptions.

## License
MIT

## Usage

1. **Backend**:
   ```bash
   cd nutricoach/backend
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix
   source venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```
2. **Frontend**:
   ```bash
   cd nutricoach/frontend
   npm install
   npm run dev
   ```
   The development server will be available at `http://localhost:5173/`.
3. Open the landing page in your browser at `http://localhost:5173/`. Fill in the form and submit to create a user via the backend API.

For production deployment, refer to the Docker setup instructions.