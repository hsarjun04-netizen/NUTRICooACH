# NutriCoach AI - Project Report

## 📋 Executive Summary

**Project Name:** NutriCoach AI  
**Version:** 2.0  
**Development Date:** 2024  
**Repository:** https://github.com/hsarjun04-netizen/NUTRICooACH.git  
**Project Type:** Full-Stack Web Application  
**Domain:** Health & Nutrition Technology  

NutriCoach AI is a comprehensive, AI-powered nutrition coaching platform that provides personalized meal planning, health tracking, and wellness management. The application combines modern web technologies with intelligent meal generation algorithms to help users achieve their health and fitness goals through data-driven nutrition guidance.

---

## 🎯 Project Objectives

1. **Personalized Nutrition:** Generate customized meal plans based on individual health profiles, dietary preferences, and medical conditions
2. **Health Tracking:** Enable users to track meals, water intake, weight, exercise, and body measurements
3. **Goal Achievement:** Provide tools for monitoring progress toward health and fitness goals
4. **User Engagement:** Implement gamification through weekly challenges to maintain user motivation
5. **Accessibility:** Create a responsive, mobile-first design with PWA capabilities

---

## 🏗️ System Architecture

### Architecture Pattern
**Client-Server Architecture** with RESTful API design

### Technology Stack

#### Frontend Technologies
- **Vue.js 3.x** - Reactive UI framework
- **Vite 4.x** - Build tool and dev server
- **Pinia 2.x** - State management
- **Vue Router 4.x** - Client-side routing
- **Chart.js 4.x** - Data visualization
- **Axios 1.x** - HTTP client
- **Vite PWA Plugin** - Progressive Web App support

#### Backend Technologies
- **Python 3.11+** - Backend runtime
- **Flask 3.x** - Web framework
- **Flask-JWT-Extended 4.x** - Authentication
- **Flask-CORS 4.x** - Cross-origin support
- **Flask-Limiter 3.x** - Rate limiting
- **Pydantic 2.x** - Data validation
- **SQLite 3.x** - Database

---

## 📦 Core Features

### 1. User Management & Authentication
- Secure JWT-based authentication
- Comprehensive user profiles with health data
- Encrypted password storage with hashing
- Token-based session handling

### 2. Health Profile & Calculations
- BMI, BMR, TDEE calculations
- Custom calorie and macronutrient targets
- Medical condition support (diabetic, low-sodium, etc.)

### 3. Meal Planning Engine
- AI-powered meal plan generation
- Indian food database with 50+ items
- Dietary preferences (Veg, Non-Veg, Vegan)
- Medical condition filtering
- Macro balancing

### 4. Food Tracking
- Daily meal logging with nutritional breakdown
- Auto-fill feature with food database
- Real-time calorie and macro tracking
- Serving size support

### 5. Water Intake Tracking
- Daily water consumption logging
- Visual circular progress indicator
- Customizable daily goals (default: 2500ml)
- Quick add (250ml increments)

### 6. Exercise Tracking
- Workout logging with duration and intensity
- Calorie burn tracking
- Exercise database with 20+ exercises
- Custom notes support

### 7. Recipe Management
- Curated recipe collection with nutritional info
- Filter by diet type, meal type, calories
- Favorites system
- Complete ingredients and instructions

### 8. Shopping List Generator
- Auto-generation from meal plans
- Category-based organization
- Quantity and unit tracking
- Purchase status marking

### 9. Progress Tracking & Analytics
- Weight and body measurement logging
- Visual charts and progress visualization
- Goal percentage tracking
- Custom date range filtering

### 10. Weekly Challenges
- Rotating weekly challenges
- Three challenge types (5 a Day, Hydration Hero, Protein Power)
- Visual progress bars
- Gamification for habit formation

### 11. Dashboard & Visualization
- Interactive central dashboard
- Real-time metrics updates
- Activity charts, donut charts, progress bars
- Monthly calendar view

### 12. UI/UX Features
- Dark/Light mode toggle
- Responsive mobile-first design
- PWA support for mobile installation
- Smooth animations and transitions
- Toast notifications

---

## 🗄️ Database Schema

### Tables (14 Total)
1. **users** - User accounts
2. **health_profiles** - Health metrics (BMI, BMR, TDEE)
3. **diet_preferences** - Dietary restrictions
4. **meal_plans** - Generated meal plans
5. **meals** - Individual meal logs
6. **weight_logs** - Weight tracking
7. **water_logs** - Water intake
8. **recipes** - Recipe database
9. **shopping_lists** - Shopping items
10. **body_measurements** - Body metrics
11. **exercise_logs** - Exercise tracking
12. **meal_reminders** - Meal notifications
13. **custom_goals** - User goals
14. **weekly_challenges** - Weekly challenges

### Features
- 25+ performance indexes
- Foreign key constraints with CASCADE deletes
- Proper data types and defaults

---

## 🔌 API Endpoints (25+)

### Authentication
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET /api/v1/auth/me
- PUT /api/v1/auth/profile
- POST /api/v1/auth/change-password

### Core Features
- GET /api/v1/dashboard/summary
- POST /api/v1/meal-plans/generate
- POST /api/v1/meals/log
- POST /api/v1/water/log
- POST /api/v1/weight/log
- POST /api/v1/exercises/log
- GET /api/v1/recipes
- POST /api/v1/shopping-list/generate
- GET /api/v1/challenges/current
- And 15+ more endpoints...

---

## 🎨 UI Components (12 Components)

1. **LandingPage** - Home page
2. **Login** - Authentication
3. **Register** - Registration
4. **Dashboard** - Main analytics hub
5. **Profile** - User profile management
6. **ProfileSetup** - Initial configuration
7. **MealPlan** - Meal plan viewer
8. **FoodTracker** - Daily meal logging
9. **ExerciseTracker** - Exercise logging
10. **Recipes** - Recipe browser
11. **ShoppingList** - Shopping management
12. **Progress** - Progress tracking

---

## 🔐 Security Features

- JWT token-based authentication
- Password hashing with Werkzeug
- Rate limiting (200/day, 50/hour)
- Pydantic data validation
- SQL injection prevention
- Comprehensive error handling
- Rotating file logs

---

## 🚀 Deployment

### Render (Configured)
- **Build:** Install dependencies + build frontend
- **Start:** Python WSGI server
- **Environment:** Python 3.11, Node 20.11

### Local Development
```bash
# Backend
cd nutricoach/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python app.py

# Frontend
cd nutricoach/frontend
npm install
npm run dev
```

---

## 📊 Project Statistics

- **Backend Code:** ~1,400 lines (Python)
- **Frontend Code:** ~5,000+ lines (Vue.js + CSS)
- **Database:** 14 tables, 25+ indexes
- **API Endpoints:** 25+ RESTful endpoints
- **UI Components:** 12 Vue components
- **Food Database:** 50+ Indian food items
- **Exercise Database:** 20+ exercises
- **Recipe Database:** 30+ recipes

---

## 🏆 Project Achievements

✅ Complete full-stack application  
✅ 25+ RESTful API endpoints with validation  
✅ AI-powered meal planning engine  
✅ Modern responsive UI with dark/light themes  
✅ PWA support for mobile installation  
✅ Comprehensive health tracking (6 categories)  
✅ Weekly challenges for engagement  
✅ Production-ready deployment configuration  
✅ Security best practices implemented  
✅ Clean, maintainable architecture  

---

## 📈 Future Enhancements

1. AI integration (OpenAI API)
2. Push notifications
3. Social features
4. Barcode scanner
5. Fitbit/Apple Health integration
6. Advanced ML analytics
7. Multi-language support
8. Premium subscription features
9. PostgreSQL migration
10. Comprehensive test suite

---

## 📝 License

**MIT License** - Open-source, free to use and modify

---

## 📞 Repository

**GitHub:** https://github.com/hsarjun04-netizen/NUTRICooACH

---

**Report Generated:** April 2026  
**Project Version:** 2.0  
**Status:** Production-Ready ✅
