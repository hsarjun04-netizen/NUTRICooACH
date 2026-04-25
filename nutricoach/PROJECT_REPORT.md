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

```
┌─────────────────────────────────────────┐
│          Frontend (Vue.js)              │
│  ┌──────────────────────────────────┐   │
│  │  Vue 3 + Vite + Pinia + Router   │   │
│  │  Chart.js + PWA Plugin           │   │
│  └──────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │ HTTP/REST API
               │ JSON
┌──────────────▼──────────────────────────┐
│          Backend (Flask)                │
│  ┌──────────────────────────────────┐   │
│  │  Flask + JWT + Pydantic          │   │
│  │  Rate Limiter + Logging          │   │
│  │  Meal Engine + Validation        │   │
│  └──────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │ SQL
┌──────────────▼──────────────────────────┐
│        Database (SQLite)                │
│  ┌──────────────────────────────────┐   │
│  │  14 Tables with Indexes          │   │
│  │  Foreign Key Constraints         │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Technology Stack

#### Frontend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| Vue.js | 3.x | Reactive UI framework |
| Vite | 4.x | Build tool and dev server |
| Pinia | 2.x | State management |
| Vue Router | 4.x | Client-side routing |
| Chart.js | 4.x | Data visualization |
| Axios | 1.x | HTTP client |
| Vite PWA Plugin | Latest | Progressive Web App support |

#### Backend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Backend runtime |
| Flask | 3.x | Web framework |
| Flask-JWT-Extended | 4.x | Authentication |
| Flask-CORS | 4.x | Cross-origin support |
| Flask-Limiter | 3.x | Rate limiting |
| Pydantic | 2.x | Data validation |
| SQLite | 3.x | Database |

---

## 📦 Core Features

### 1. User Management & Authentication
- **Registration & Login:** Secure JWT-based authentication
- **Profile Management:** Comprehensive user profiles with health data
- **Password Security:** Encrypted password storage with hashing
- **Session Management:** Token-based session handling with localStorage

### 2. Health Profile & Calculations
- **BMI Calculation:** Body Mass Index computation
- **BMR Calculation:** Basal Metabolic Rate using standard formulas
- **TDEE Calculation:** Total Daily Energy Expenditure based on activity level
- **Custom Goals:** Personalized calorie and macronutrient targets
- **Medical Conditions:** Support for dietary restrictions (diabetic, low-sodium, etc.)

### 3. Meal Planning Engine
- **AI-Powered Generation:** Rule-based meal plan generation using Indian food database
- **Dietary Preferences:** Supports Vegetarian, Non-Vegetarian, and Vegan diets
- **Medical Condition Filtering:** Filters meals based on health conditions
- **Macro Balancing:** Ensures balanced macronutrient distribution
- **Meal Types:** Breakfast, Lunch, Dinner, and Snacks
- **Database:** 50+ Indian food items with nutritional information

### 4. Food Tracking
- **Daily Meal Logging:** Track meals with complete nutritional breakdown
- **Auto-Fill Feature:** Food database for quick meal entry
- **Nutritional Summary:** Real-time calorie and macro tracking
- **Meal Categories:** Organized by meal type
- **Serving Sizes:** Support for multiple servings

### 5. Water Intake Tracking
- **Daily Logging:** Track water consumption in milliliters
- **Visual Progress:** Circular progress indicator
- **Goal Setting:** Customizable daily water goals (default: 2500ml)
- **Quick Add:** One-tap water logging (250ml increments)

### 6. Exercise Tracking
- **Exercise Logging:** Record workouts with duration and intensity
- **Calorie Burn Tracking:** Monitor calories burned during exercise
- **Exercise Database:** Pre-populated with common exercises
- **Notes Support:** Add custom notes for each workout
- **History View:** View past exercise logs

### 7. Recipe Management
- **Recipe Database:** Curated collection of healthy recipes
- **Nutritional Information:** Complete macro breakdown per recipe
- **Filtering:** Filter by diet type, meal type, and calories
- **Favorites:** Save favorite recipes for quick access
- **Recipe Details:** Ingredients, instructions, prep/cook time
- **Servings Information:** Quantity and portion details

### 8. Shopping List Generator
- **Auto-Generation:** Generate shopping lists from meal plans
- **Categorization:** Items organized by category (Protein, Grains, Vegetables, etc.)
- **Quantity Tracking:** Track item quantities and units
- **Purchase Status:** Mark items as purchased
- **Meal Plan Integration:** Linked to weekly meal plans

### 9. Progress Tracking & Analytics
- **Weight Logging:** Track weight over time
- **Body Measurements:** Record body fat, waist, hips, chest, arms, thighs
- **Visual Charts:** Line charts for progress visualization
- **Goal Progress:** Percentage completion tracking
- **Date Range Filtering:** View progress over custom periods

### 10. Weekly Challenges (NEW)
- **Rotating Challenges:** New challenge every week
- **Challenge Types:**
  - 5 a Day Challenge (fruits & vegetables)
  - Hydration Hero (water intake)
  - Protein Power (protein goals)
- **Progress Tracking:** Visual progress bars with percentages
- **Goal Setting:** Weekly targets with unit tracking
- **Gamification:** Encourages healthy habit formation

### 11. Dashboard & Visualization
- **Interactive Dashboard:** Central hub for all health metrics
- **Real-Time Data:** Live updates of tracked metrics
- **Charts & Graphs:**
  - Daily activity chart (calorie consumption over time)
  - Donut chart (calorie budget: eaten vs. remaining)
  - Progress bars (macro distribution)
- **Calendar View:** Monthly calendar with activity highlights
- **Hero Banner:** Featured weekly challenge display

### 12. UI/UX Features
- **Dark/Light Mode:** Toggle between themes
- **Responsive Design:** Mobile-first, works on all devices
- **PWA Support:** Installable as mobile app
- **Skeleton Loading:** Smooth loading animations
- **Toast Notifications:** Success/error feedback
- **Smooth Animations:** CSS transitions and keyframe animations
- **Sidebar Navigation:** Icon-based navigation with labels

---

## 🗄️ Database Schema

### Tables Overview (14 Tables)

| Table Name | Purpose | Key Fields |
|------------|---------|------------|
| **users** | User accounts | id, name, email, password_hash, age, gender, diet_type |
| **health_profiles** | Health metrics | user_id, bmi, bmr, tdee, target_calories |
| **diet_preferences** | Dietary restrictions | user_id, allergies, macronutrient_goals |
| **meal_plans** | Generated meal plans | user_id, date, total_calories |
| **meals** | Individual meals | user_id, name, calories, protein, carbs, fats, meal_type |
| **weight_logs** | Weight tracking | user_id, weight, date |
| **water_logs** | Water intake | user_id, amount_ml, date |
| **recipes** | Recipe database | name, calories, ingredients, instructions, diet_type |
| **shopping_lists** | Shopping items | user_id, item_name, category, quantity, is_purchased |
| **body_measurements** | Body metrics | user_id, body_fat, waist, hips, chest, arms, thighs |
| **exercise_logs** | Exercise tracking | user_id, exercise_name, duration_minutes, calories_burned |
| **meal_reminders** | Meal notifications | user_id, meal_type, reminder_time, is_enabled |
| **custom_goals** | User goals | user_id, water_goal_ml, calorie_goal, protein_goal |
| **weekly_challenges** | Weekly challenges | user_id, title, goal, current_progress, week_start_date |

### Database Features
- **Foreign Key Constraints:** Referential integrity with CASCADE deletes
- **Indexes:** 25+ performance indexes on frequently queried columns
- **Data Types:** Appropriate use of INTEGER, REAL, TEXT, DATE, TIMESTAMP, BOOLEAN
- **Auto-Increment:** Primary keys with AUTOINCREMENT
- **Default Values:** Sensible defaults for timestamps and boolean flags

---

## 🔌 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user profile
- `PUT /api/v1/auth/profile` - Update profile
- `POST /api/v1/auth/change-password` - Change password

### Dashboard & Summary
- `GET /api/v1/dashboard/summary` - Get dashboard summary

### Meal Planning
- `POST /api/v1/meal-plans/generate` - Generate meal plan
- `GET /api/v1/meal-plans/current` - Get current meal plan

### Food Tracking
- `POST /api/v1/meals/log` - Log a meal
- `GET /api/v1/meals/today` - Get today's meals

### Water Tracking
- `POST /api/v1/water/log` - Log water intake
- `GET /api/v1/water/today` - Get today's water intake

### Weight Tracking
- `POST /api/v1/weight/log` - Log weight
- `GET /api/v1/weight/history` - Get weight history

### Exercise Tracking
- `POST /api/v1/exercises/log` - Log exercise
- `GET /api/v1/exercises/history` - Get exercise history

### Recipes
- `GET /api/v1/recipes` - Get all recipes
- `GET /api/v1/recipes/:id` - Get recipe details
- `GET /api/v1/recipes/suggestions` - Get personalized suggestions
- `POST /api/v1/recipes/:id/favorite` - Toggle favorite

### Shopping List
- `POST /api/v1/shopping-list/generate` - Generate shopping list
- `GET /api/v1/shopping-list` - Get shopping list
- `PUT /api/v1/shopping-list/:id` - Update item
- `DELETE /api/v1/shopping-list/:id` - Delete item

### Progress & Measurements
- `POST /api/v1/measurements` - Log body measurements
- `GET /api/v1/measurements/history` - Get measurement history
- `GET /api/v1/progress` - Get progress data

### Weekly Challenges
- `GET /api/v1/challenges/current` - Get current challenge
- `POST /api/v1/challenges/update` - Update challenge progress

### Data Export
- `GET /api/v1/export/data` - Export user data (CSV)
- `POST /api/v1/backup` - Create database backup

---

## 🎨 User Interface Components

### Frontend Components (12 Components)

| Component | File | Purpose |
|-----------|------|---------|
| LandingPage | `LandingPage.vue` | Home page with feature overview |
| Login | `Login.vue` | User authentication |
| Register | `Register.vue` | User registration |
| Dashboard | `Dashboard.vue` | Main dashboard with analytics |
| Profile | `Profile.vue` | User profile management |
| ProfileSetup | `ProfileSetup.vue` | Initial profile configuration |
| MealPlan | `MealPlan.vue` | View and manage meal plans |
| FoodTracker | `FoodTracker.vue` | Daily meal logging |
| ExerciseTracker | `ExerciseTracker.vue` | Exercise logging and history |
| Recipes | `Recipes.vue` | Recipe browser and details |
| ShoppingList | `ShoppingList.vue` | Shopping list management |
| Progress | `Progress.vue` | Progress tracking and charts |

### UI Design Features
- **CSS Variables:** Consistent theming with custom properties
- **Modern Design:** Card-based layout with shadows and rounded corners
- **Color Scheme:** 
  - Primary: Lime Green (#a3e635)
  - Light Mode: Slate grays and whites
  - Dark Mode: Dark slate and navy
- **Typography:** Clean, readable fonts with proper hierarchy
- **Spacing:** Consistent padding and margins using CSS variables
- **Animations:** 
  - Fade-in-up entrance animations
  - Hover effects with transforms
  - Loading skeleton screens
  - Smooth transitions on all interactive elements

---

## 🔐 Security Features

### Authentication & Authorization
- **JWT Tokens:** Stateless authentication with Flask-JWT-Extended
- **Password Hashing:** Werkzeug's `generate_password_hash` with salt
- **Token Expiration:** Configurable token lifetime
- **Protected Routes:** Frontend route guards + backend JWT validation
- **Session Management:** Secure token storage in localStorage

### Data Validation
- **Pydantic Models:** Strict data validation on all API inputs
- **Input Sanitization:** Custom validation functions
- **SQL Injection Prevention:** Parameterized queries
- **Type Checking:** Python type hints throughout

### Rate Limiting
- **Default Limits:** 200 requests per day, 50 per hour
- **Endpoint-Specific:** Stricter limits on sensitive endpoints
- **Memory Storage:** In-memory rate limiter for performance

### Error Handling
- **Global Error Handlers:** 400, 401, 404, 429, 500 error handlers
- **Structured Responses:** Consistent JSON error format
- **Logging:** Rotating file logs with separate error log
- **User-Friendly Messages:** Clear error messages without exposing internals

---

## 📊 Performance Optimizations

### Frontend
- **Code Splitting:** Lazy-loaded route components
- **Tree Shaking:** Unused code elimination via Vite
- **Asset Optimization:** Compressed images and fonts
- **PWA Caching:** Service worker for offline support
- **Debounced Inputs:** Reduced API calls on form inputs

### Backend
- **Database Indexes:** 25+ indexes for fast queries
- **Connection Management:** Proper DB connection opening/closing
- **Pagination:** Support for paginated results
- **Caching Strategy:** PWA cache for static assets
- **Efficient Queries:** Optimized SQL with proper joins

### Build Configuration
- **Vite:** Fast HMR (Hot Module Replacement)
- **Production Build:** Minified and optimized assets
- **Environment Variables:** Secure configuration management

---

## 🚀 Deployment

### Deployment Configuration
- **Platform:** Render (render.yaml configured)
- **Build Command:** 
  ```bash
  cd nutricoach/backend && pip install -r requirements.txt
  cd ../frontend && npm install && npm run build
  ```
- **Start Command:** `cd nutricoach/backend && python wsgi.py`
- **Environment Variables:**
  - `PYTHON_VERSION`: 3.11.0
  - `NODE_VERSION`: 20.11.0
  - `FLASK_ENV`: production
  - `JWT_SECRET_KEY`: Auto-generated

### Deployment Options
1. **Render** (Configured) - Recommended for production
2. **Docker** (Supported) - Containerized deployment
3. **Heroku** - Alternative PaaS option
4. **VPS** - Manual deployment on any Linux server

### Local Development
```bash
# Backend
cd nutricoach/backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python init_db.py
python app.py

# Frontend
cd nutricoach/frontend
npm install
npm run dev
```

---

## 📈 Project Statistics

### Code Metrics
- **Total Files:** 40+ files
- **Backend Code:** ~1,400 lines (Python)
- **Frontend Code:** ~5,000+ lines (Vue.js + CSS)
- **Database Schema:** 14 tables, 25+ indexes
- **API Endpoints:** 25+ RESTful endpoints
- **UI Components:** 12 Vue components

### Data & Content
- **Food Database:** 50+ Indian food items
- **Exercise Database:** 20+ exercises
- **Recipe Database:** 30+ recipes (seeded)
- **Challenge Types:** 3 rotating weekly challenges

### Version Control
- **Platform:** GitHub
- **Repository:** https://github.com/hsarjun04-netizen/NUTRICooACH
- **Branches:** main
- **Commits:** Regular commits with descriptive messages

---

## 🧪 Testing & Quality Assurance

### Validation Layers
1. **Frontend Validation:** Form validation with required fields
2. **API Validation:** Pydantic models for request/response validation
3. **Database Constraints:** Foreign keys, unique constraints, NOT NULL
4. **Business Logic:** Meal engine rules and filtering

### Error Prevention
- **Try-Catch Blocks:** Comprehensive error handling
- **Null Checks:** Defensive programming throughout
- **Type Safety:** Python type hints and Pydantic validation
- **Consistent Responses:** Standardized API response format

---

## 🔄 Future Enhancements

### Recommended Features
1. **AI Integration:** OpenAI API for personalized nutrition advice
2. **Push Notifications:** Meal reminders and challenge updates
3. **Social Features:** Share progress, compete with friends
4. **Barcode Scanner:** Quick food logging via barcode scanning
5. **Meal Photo Logging:** Image-based meal tracking
6. **Integration APIs:** Fitbit, Apple Health, Google Fit
7. **Advanced Analytics:** Machine learning for trend prediction
8. **Multi-Language Support:** Internationalization (i18n)
9. **Payment Integration:** Premium subscription features
10. **Admin Dashboard:** User management and analytics

### Technical Improvements
1. **Database Migration:** SQLite → PostgreSQL for production
2. **Caching Layer:** Redis for session management and caching
3. **API Versioning:** Structured API versioning strategy
4. **Unit Tests:** Comprehensive test suite (pytest)
5. **E2E Tests:** Cypress or Playwright for frontend testing
6. **CI/CD Pipeline:** Automated testing and deployment
7. **Monitoring:** Sentry for error tracking, Analytics for usage
8. **Documentation:** Swagger/OpenAPI for API documentation

---

## 📚 Project Documentation

### Available Documentation
1. **README.md:** Project overview and setup instructions
2. **API.md:** Detailed API endpoint documentation
3. **TECHNICAL_UPGRADES.md:** Technical implementation details
4. **UI_UPGRADE_GUIDE.md:** UI/UX design documentation
5. **Project Report (This File):** Comprehensive project overview

### Code Organization
```
nutricoach/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── meal_engine.py         # Meal plan generation logic
│   ├── validation.py          # Input validation functions
│   ├── backup.py              # Database backup utilities
│   ├── init_db.py             # Database initialization
│   ├── seed_recipes.py        # Recipe database seeder
│   ├── schema.sql             # Complete database schema
│   ├── requirements.txt       # Python dependencies
│   ├── wsgi.py                # WSGI entry point
│   └── logs/                  # Application logs
├── frontend/
│   ├── src/
│   │   ├── components/        # Shared components
│   │   ├── stores/            # Pinia stores (auth, theme, user)
│   │   ├── styles/            # Global CSS
│   │   ├── App.vue            # Root component
│   │   ├── main.js            # Application entry
│   │   ├── router.js          # Vue Router configuration
│   │   └── api.js             # API client
│   ├── components/            # Page components
│   ├── index.html             # HTML entry point
│   ├── vite.config.js         # Vite configuration
│   └── package.json           # NPM dependencies
├── render.yaml                # Render deployment config
└── .gitignore                 # Git ignore rules
```

---

## 👥 Development Team

**Developer:** Single Full-Stack Developer  
**Development Period:** 2024  
**Development Approach:** Agile, Iterative Development  

---

## 📝 License

**License Type:** MIT License  
**Usage:** Open-source, free to use, modify, and distribute  

---

## 🎓 Learning Outcomes

### Technologies Mastered
1. Vue.js 3 Composition API and Options API
2. Flask RESTful API development
3. JWT authentication implementation
4. SQLite database design and optimization
5. Responsive UI/UX design with CSS3
6. Progressive Web App (PWA) implementation
7. Data visualization with Chart.js
8. State management with Pinia
9. Build tools (Vite, npm)
10. Version control with Git and GitHub

### Development Skills
- Full-stack web development
- RESTful API design
- Database schema design
- Security best practices
- Performance optimization
- Responsive design
- Code organization and architecture
- Documentation writing

---

## 🏆 Project Achievements

✅ Complete full-stack application with 14 database tables  
✅ 25+ RESTful API endpoints with validation  
✅ AI-powered meal planning engine with 50+ food items  
✅ Modern, responsive UI with dark/light themes  
✅ PWA support for mobile installation  
✅ Comprehensive health tracking (meals, water, exercise, weight, measurements)  
✅ Recipe database with filtering and favorites  
✅ Shopping list auto-generation  
✅ Weekly challenges for user engagement  
✅ Security features (JWT, password hashing, rate limiting)  
✅ Production-ready deployment configuration  
✅ Comprehensive logging and error handling  
✅ Clean, maintainable code architecture  

---

## 📞 Contact & Support

**Repository:** https://github.com/hsarjun04-netizen/NUTRICooACH  
**Issues:** Report bugs and feature requests via GitHub Issues  
**Documentation:** See project documentation files for detailed guides  

---

## 📊 Conclusion

NutriCoach AI represents a comprehensive, production-ready nutrition coaching platform that successfully combines modern web technologies with intelligent meal planning algorithms. The application demonstrates proficiency in full-stack development, database design, security implementation, and user experience design.

With its modular architecture, extensive feature set, and scalable design, NutriCoach AI provides a solid foundation for further enhancements and can serve as a portfolio piece demonstrating advanced web development capabilities.

The project is ready for deployment and can be easily extended with additional features such as AI integration, social features, and advanced analytics to meet evolving user needs.

---

**Report Generated:** April 2026  
**Project Version:** 2.0  
**Status:** Production-Ready ✅
