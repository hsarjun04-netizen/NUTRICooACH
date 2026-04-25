# API Endpoints Reference

<cite>
**Referenced Files in This Document**
- [API.md](file://nutricoach/backend/API.md)
- [app.py](file://nutricoach/backend/app.py)
- [init_db.py](file://nutricoach/backend/init_db.py)
- [schema.sql](file://nutricoach/backend/schema.sql)
- [LandingPage.vue](file://nutricoach/frontend/components/LandingPage.vue)
- [Dashboard.vue](file://nutricoach/frontend/components/Dashboard.vue)
- [api.js](file://nutricoach/frontend/src/api.js)
- [README.md](file://nutricoach/README.md)
</cite>

## Update Summary
**Changes Made**
- Added new Water Intake Tracking API endpoints section
- Updated Dashboard Summary section to include water metrics
- Enhanced authentication requirements for water endpoints
- Added water intake data model and examples
- Updated frontend integration examples for water tracking

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Dependency Analysis](#dependency-analysis)
7. [Performance Considerations](#performance-considerations)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Conclusion](#conclusion)

## Introduction
This document provides a comprehensive reference for the NutriCoach AI REST API. It covers endpoint definitions, HTTP methods, URL patterns, request/response schemas, authentication requirements, and practical client usage examples. The API follows a versioned base path and exposes endpoints for user management, dietary preferences, meal plans, authentication, and water intake tracking.

## Project Structure
The API is implemented in a Python Flask backend with SQLite persistence. The frontend demonstrates client-side consumption of the API. The backend defines the base URL and endpoint list, while the frontend consumes the user creation endpoint and water tracking features.

```mermaid
graph TB
FE["Frontend (Vue.js)"]
BE["Backend (Flask)"]
DB["SQLite Database"]
FE --> |"HTTP requests"| BE
BE --> |"Database operations"| DB
```

**Section sources**
- [README.md:49-50](file://nutricoach/README.md#L49-L50)
- [API.md:3](file://nutricoach/backend/API.md#L3)

## Core Components
- Base URL: `/api/v1`
- Versioning strategy: Path-based versioning using `/api/v1`.
- Authentication: JWT-based authentication required for water tracking endpoints.
- Rate limiting: Not implemented in the current backend.
- Pagination: Not implemented in the current backend.

**Section sources**
- [API.md:3](file://nutricoach/backend/API.md#L3)
- [app.py:1-31](file://nutricoach/backend/app.py#L1-L31)
- [api.js:10-17](file://nutricoach/frontend/src/api.js#L10-L17)

## Architecture Overview
The API follows a simple request-response pattern. Clients send HTTP requests to the backend, which performs database operations and returns JSON responses. Water tracking endpoints require JWT authentication for security.

```mermaid
sequenceDiagram
participant Client as "Client"
participant Flask as "Flask App"
participant DB as "SQLite"
Client->>Flask : "POST /api/v1/water/log"
Flask->>DB : "Insert water log record"
DB-->>Flask : "Success"
Flask-->>Client : "201 Created with message"
```

**Diagram sources**
- [app.py:513-527](file://nutricoach/backend/app.py#L513-L527)

## Detailed Component Analysis

### User Management Endpoints
- Base path: `/api/v1/users`

Endpoints:
- POST `/api/v1/users`
  - Purpose: Create a new user.
  - Authentication: Not required.
  - Request body (JSON):
    - name: string, required
    - email: string, required
    - age: integer, optional
    - weight: number, optional
    - height: number, optional
    - goals: string, optional
  - Success response (201 Created):
    - Body: `{ "id": integer }`
  - Error responses:
    - 400 Bad Request: Validation errors or malformed JSON.
    - 500 Internal Server Error: Database or server issues.
  - Example curl:
    - curl -X POST http://localhost:5000/api/v1/users -H "Content-Type: application/json" -d '{"name":"John Doe","email":"user@example.com","age":30,"weight":70.5,"height":175.0,"goals":"weight-loss"}'
  - Example JavaScript (fetch):
    - fetch('http://localhost:5000/api/v1/users', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name: "John Doe", email: "user@example.com", age: 30, weight: 70.5, height: 175.0, goals: "weight-loss" }) }).then(r => r.json()).then(console.log);

- GET `/api/v1/users/{user_id}`
  - Purpose: Retrieve user details by ID.
  - Authentication: Not required.
  - Path parameters:
    - user_id: integer, required
  - Success response (200 OK):
    - Body: User object matching the schema below.
  - Error responses:
    - 404 Not Found: User not found.
    - 500 Internal Server Error: Database or server issues.
  - Example curl:
    - curl http://localhost:5000/api/v1/users/1
  - Example JavaScript (fetch):
    - fetch('http://localhost:5000/api/v1/users/1').then(r => r.json()).then(console.log);

- PUT `/api/v1/users/{user_id}`
  - Purpose: Update user details by ID.
  - Authentication: Not required.
  - Path parameters:
    - user_id: integer, required
  - Request body (JSON):
    - name: string, optional
    - email: string, optional
    - age: integer, optional
    - weight: number, optional
    - height: number, optional
    - goals: string, optional
  - Success response (200 OK):
    - Body: Updated user object.
  - Error responses:
    - 404 Not Found: User not found.
    - 400 Bad Request: Validation errors or malformed JSON.
    - 500 Internal Server Error: Database or server issues.
  - Example curl:
    - curl -X PUT http://localhost:5000/api/v1/users/1 -H "Content-Type: application/json" -d '{"goals":"muscle-gain"}'
  - Example JavaScript (fetch):
    - fetch('http://localhost:5000/api/v1/users/1', { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ goals: "muscle-gain" }) }).then(r => r.json()).then(console.log);

- DELETE `/api/v1/users/{user_id}`
  - Purpose: Delete a user by ID.
  - Authentication: Not required.
  - Path parameters:
    - user_id: integer, required
  - Success response (204 No Content):
    - Body: Empty.
  - Error responses:
    - 404 Not Found: User not found.
    - 500 Internal Server Error: Database or server issues.
  - Example curl:
    - curl -X DELETE http://localhost:5000/api/v1/users/1
  - Example JavaScript (fetch):
    - fetch('http://localhost:5000/api/v1/users/1', { method: 'DELETE' });

Notes:
- The backend currently implements only POST for user creation. Other methods are described per the API specification but may require additional implementation.

**Section sources**
- [API.md:6-10](file://nutricoach/backend/API.md#L6-L10)
- [app.py:16-26](file://nutricoach/backend/app.py#L16-L26)

### Authentication Endpoints
- Base path: `/api/v1/auth`

Endpoints:
- POST `/api/v1/auth/register`
  - Purpose: Register a new user account.
  - Authentication: Not required.
  - Request body (JSON):
    - name: string, required
    - email: string, required
    - password: string, required
  - Success response (201 Created):
    - Body: `{ "message": "User registered successfully" }`
  - Error responses:
    - 400 Bad Request: Validation errors or missing fields.
    - 500 Internal Server Error: Database or server issues.
  - Example curl:
    - curl -X POST http://localhost:5000/api/v1/auth/register -H "Content-Type: application/json" -d '{"name":"Jane Doe","email":"jane@example.com","password":"securePass"}'
  - Example JavaScript (fetch):
    - fetch('http://localhost:5000/api/v1/auth/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name: "Jane Doe", email: "jane@example.com", password: "securePass" }) }).then(r => r.json()).then(console.log);

- POST `/api/v1/auth/login`
  - Purpose: Authenticate user and return a token.
  - Authentication: Not required.
  - Request body (JSON):
    - email: string, required
    - password: string, required
  - Success response (200 OK):
    - Body: `{ "token": "string" }`
  - Error responses:
    - 400 Bad Request: Validation errors or missing fields.
    - 401 Unauthorized: Invalid credentials.
    - 500 Internal Server Error: Database or server issues.
  - Example curl:
    - curl -X POST http://localhost:5000/api/v1/auth/login -H "Content-Type: application/json" -d '{"email":"jane@example.com","password":"securePass"}'
  - Example JavaScript (fetch):
    - fetch('http://localhost:5000/api/v1/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: "jane@example.com", password: "securePass" }) }).then(r => r.json()).then(console.log);

Notes:
- Token handling and bearer authentication are implemented in the frontend API interceptor.

**Section sources**
- [API.md:21-23](file://nutricoach/backend/API.md#L21-L23)
- [api.js:10-17](file://nutricoach/frontend/src/api.js#L10-L17)

### Dietary Preferences Endpoints
- Base path: `/api/v1/diet-preferences`

Endpoints:
- POST `/api/v1/diet-preferences`
  - Purpose: Set or update diet preferences for a user.
  - Authentication: Not required.
  - Request body (JSON):
    - user_id: integer, required
    - allergies: string, optional
    - dietary_restrictions: string, optional
    - macronutrient_goals: string, optional
  - Success response (201 Created):
    - Body: `{ "message": "Preferences saved" }`
  - Error responses:
    - 400 Bad Request: Validation errors or missing fields.
    - 500 Internal Server Error: Database or server issues.
  - Example curl:
    - curl -X POST http://localhost:5000/api/v1/diet-preferences -H "Content-Type: application/json" -d '{"user_id":1,"allergies":"none","dietary_restrictions":"vegetarian","macronutrient_goals":"balanced"}'
  - Example JavaScript (fetch):
    - fetch('http://localhost:5000/api/v1/diet-preferences', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ user_id: 1, allergies: "none", dietary_restrictions: "vegetarian", macronutrient_goals: "balanced" }) }).then(r => r.json()).then(console.log);

- GET `/api/v1/diet-preferences/{user_id}`
  - Purpose: Get diet preferences for a user.
  - Authentication: Not required.
  - Path parameters:
    - user_id: integer, required
  - Success response (200 OK):
    - Body: Dietary preferences object matching the schema below.
  - Error responses:
    - 404 Not Found: Preferences not found.
    - 500 Internal Server Error: Database or server issues.
  - Example curl:
    - curl http://localhost:5000/api/v1/diet-preferences/1
  - Example JavaScript (fetch):
    - fetch('http://localhost:5000/api/v1/diet-preferences/1').then(r => r.json()).then(console.log);

Notes:
- The backend does not implement these endpoints yet.

**Section sources**
- [API.md:12-14](file://nutricoach/backend/API.md#L12-L14)

### Meal Plan Endpoints
- Base path: `/api/v1/meal-plans`

Endpoints:
- POST `/api/v1/meal-plans`
  - Purpose: Generate and save a personalized meal plan.
  - Authentication: Not required.
  - Request body (JSON):
    - user_id: integer, required
    - date: date, required
    - meals: string, required
  - Success response (201 Created):
    - Body: `{ "message": "Meal plan saved" }`
  - Error responses:
    - 400 Bad Request: Validation errors or missing fields.
    - 500 Internal Server Error: Database or server issues.
  - Example curl:
    - curl -X POST http://localhost:5000/api/v1/meal-plans -H "Content-Type: application/json" -d '{"user_id":1,"date":"2025-06-15","meals":"breakfast: omelet\\nlunch: salad\\ndinner: fish"}'
  - Example JavaScript (fetch):
    - fetch('http://localhost:5000/api/v1/meal-plans', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ user_id: 1, date: "2025-06-15", meals: "breakfast: omelet\nlunch: salad\ndinner: fish" }) }).then(r => r.json()).then(console.log);

- GET `/api/v1/meal-plans/{user_id}`
  - Purpose: Retrieve the latest meal plan for a user.
  - Authentication: Not required.
  - Path parameters:
    - user_id: integer, required
  - Success response (200 OK):
    - Body: Latest meal plan object matching the schema below.
  - Error responses:
    - 404 Not Found: No meal plan found.
    - 500 Internal Server Error: Database or server issues.
  - Example curl:
    - curl http://localhost:5000/api/v1/meal-plans/1
  - Example JavaScript (fetch):
    - fetch('http://localhost:5000/api/v1/meal-plans/1').then(r => r.json()).then(console.log);

- GET `/api/v1/meal-plans/{user_id}/history`
  - Purpose: Retrieve meal plan history for a user.
  - Authentication: Not required.
  - Path parameters:
    - user_id: integer, required
  - Success response (200 OK):
    - Body: Array of meal plan objects matching the schema below.
  - Error responses:
    - 404 Not Found: No history found.
    - 500 Internal Server Error: Database or server issues.
  - Example curl:
    - curl http://localhost:5000/api/v1/meal-plans/1/history
  - Example JavaScript (fetch):
    - fetch('http://localhost:5000/api/v1/meal-plans/1/history').then(r => r.json()).then(console.log);

Notes:
- The backend does not implement these endpoints yet.

**Section sources**
- [API.md:16-19](file://nutricoach/backend/API.md#L16-L19)

### Water Intake Tracking Endpoints
- Base path: `/api/v1/water`

**Authentication Required**: All water tracking endpoints require JWT authentication.

Endpoints:
- POST `/api/v1/water/log`
  - Purpose: Log water intake for the authenticated user.
  - Authentication: Required (JWT).
  - Request body (JSON):
    - amount_ml: integer, optional (defaults to 250)
    - date: string (ISO format), optional (defaults to today)
  - Success response (201 Created):
    - Body: `{ "message": "Water logged" }`
  - Error responses:
    - 400 Bad Request: Validation errors or missing fields.
    - 401 Unauthorized: Invalid or missing JWT token.
    - 500 Internal Server Error: Database or server issues.
  - Example curl:
    - curl -X POST http://localhost:5000/api/v1/water/log -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_JWT_TOKEN" -d '{"amount_ml": 500, "date": "2025-06-15"}'
  - Example JavaScript (fetch):
    - fetch('http://localhost:5000/api/v1/water/log', { method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer YOUR_JWT_TOKEN' }, body: JSON.stringify({ amount_ml: 500, date: "2025-06-15" }) }).then(r => r.json()).then(console.log);

- GET `/api/v1/water/today`
  - Purpose: Get today's total water intake for the authenticated user.
  - Authentication: Required (JWT).
  - Success response (200 OK):
    - Body: `{ "total_ml": integer, "entries": integer }`
  - Error responses:
    - 401 Unauthorized: Invalid or missing JWT token.
    - 500 Internal Server Error: Database or server issues.
  - Example curl:
    - curl http://localhost:5000/api/v1/water/today -H "Authorization: Bearer YOUR_JWT_TOKEN"
  - Example JavaScript (fetch):
    - fetch('http://localhost:5000/api/v1/water/today', { headers: { 'Authorization': 'Bearer YOUR_JWT_TOKEN' } }).then(r => r.json()).then(console.log);

Notes:
- Water logs are stored in the `water_logs` table with automatic timestamps.
- The default amount is 250ml per entry.
- Water tracking is integrated into the dashboard summary endpoint.

**Section sources**
- [app.py:511-542](file://nutricoach/backend/app.py#L511-L542)
- [schema.sql:78-85](file://nutricoach/backend/schema.sql#L78-L85)

### Dashboard Summary Endpoints
- Base path: `/api/v1/dashboard`

Enhanced with water intake metrics:

- GET `/api/v1/dashboard/summary`
  - Purpose: Retrieve comprehensive dashboard summary including water metrics.
  - Authentication: Not required.
  - Success response (200 OK):
    - Body: Dashboard summary object with water intake included.
  - Error responses:
    - 404 Not Found: User not found.
    - 500 Internal Server Error: Database or server issues.
  - Example curl:
    - curl http://localhost:5000/api/v1/dashboard/summary
  - Example JavaScript (fetch):
    - fetch('http://localhost:5000/api/v1/dashboard/summary').then(r => r.json()).then(console.log);

Dashboard summary fields include:
- name: string (user name)
- goal: string (user goals)
- bmi: number (body mass index)
- bmr: number (basal metabolic rate)
- target_calories: number (daily calorie target)
- consumed_calories: number (calories consumed)
- remaining_calories: number (calories remaining)
- latest_weight: number (latest recorded weight)
- goal_progress_percent: number (goal progress percentage)
- **water_intake: number (total water intake in ml)**

**Section sources**
- [app.py:479-508](file://nutricoach/backend/app.py#L479-L508)

### Data Models
- User
  - Fields:
    - id: integer
    - name: string
    - email: string
    - age: integer
    - weight: number
    - height: number
    - goals: string

- DietPreference
  - Fields:
    - user_id: integer
    - allergies: string
    - dietary_restrictions: string
    - macronutrient_goals: string

- MealPlan
  - Fields:
    - id: integer
    - user_id: integer
    - date: date
    - meals: string

- **WaterLog** *(New)*
  - Fields:
    - id: integer
    - user_id: integer
    - amount_ml: integer (default: 250)
    - date: date
    - created_at: timestamp

**Section sources**
- [API.md:27-59](file://nutricoach/backend/API.md#L27-L59)
- [schema.sql:78-85](file://nutricoach/backend/schema.sql#L78-L85)

## Dependency Analysis
The backend depends on SQLite for persistence and exposes endpoints defined in the API specification. The frontend consumes the user creation endpoint and water tracking features. JWT authentication is handled by the frontend API interceptor.

```mermaid
graph TB
subgraph "Backend"
APP["Flask App (app.py)"]
DB_INIT["Database Init (init_db.py)"]
SCHEMA["Schema (schema.sql)"]
WATER["Water Endpoints"]
DASHBOARD["Dashboard Summary"]
END
subgraph "Frontend"
LP["LandingPage.vue"]
DASH["Dashboard.vue"]
API["api.js (JWT Interceptor)"]
END
LP --> |"POST /api/v1/users"| APP
DASH --> |"GET /api/v1/water/today"| WATER
DASH --> |"POST /api/v1/water/log"| WATER
DASH --> |"GET /api/v1/dashboard/summary"| DASHBOARD
API --> APP
APP --> DB_INIT
DB_INIT --> SCHEMA
```

**Diagram sources**
- [app.py:1-31](file://nutricoach/backend/app.py#L1-L31)
- [init_db.py:1-47](file://nutricoach/backend/init_db.py#L1-L47)
- [schema.sql:1-25](file://nutricoach/backend/schema.sql#L1-L25)
- [LandingPage.vue:47-48](file://nutricoach/frontend/components/LandingPage.vue#L47-L48)
- [Dashboard.vue:187-202](file://nutricoach/frontend/components/Dashboard.vue#L187-L202)
- [api.js:10-17](file://nutricoach/frontend/src/api.js#L10-L17)

**Section sources**
- [app.py:1-31](file://nutricoach/backend/app.py#L1-L31)
- [init_db.py:1-47](file://nutricoach/backend/init_db.py#L1-L47)
- [schema.sql:1-25](file://nutricoach/backend/schema.sql#L1-L25)
- [LandingPage.vue:47-48](file://nutricoach/frontend/components/LandingPage.vue#L47-L48)
- [Dashboard.vue:187-202](file://nutricoach/frontend/components/Dashboard.vue#L187-L202)
- [api.js:10-17](file://nutricoach/frontend/src/api.js#L10-L17)

## Performance Considerations
- Current implementation uses SQLite with basic CRUD operations. No caching or advanced indexing is present.
- Water tracking endpoints are lightweight and should scale well with proper indexing.
- Recommendations (not implemented):
  - Add pagination for list endpoints.
  - Implement rate limiting at the Flask level.
  - Add database indexes for frequently queried columns (water_logs.user_id, water_logs.date).
  - Introduce connection pooling and transaction batching.
  - Add JWT token caching to reduce authentication overhead.

## Troubleshooting Guide
Common issues and resolutions:
- 404 Not Found:
  - Cause: Incorrect endpoint path or missing resource.
  - Resolution: Verify base URL and path parameters.
- 400 Bad Request:
  - Cause: Malformed JSON or missing required fields.
  - Resolution: Validate request payload against data models.
- 401 Unauthorized:
  - Cause: Missing or invalid JWT token for protected endpoints.
  - Resolution: Ensure JWT token is included in Authorization header and is valid.
- 500 Internal Server Error:
  - Cause: Database or server exceptions.
  - Resolution: Check server logs and database connectivity.

**Section sources**
- [API.md:21-23](file://nutricoach/backend/API.md#L21-L23)
- [api.js:20-29](file://nutricoach/frontend/src/api.js#L20-L29)

## Conclusion
The NutriCoach AI API provides a clear set of endpoints for user management, dietary preferences, meal plans, authentication, and water intake tracking under a versioned base path. The water tracking feature includes JWT authentication, comprehensive logging capabilities, and integration with the dashboard summary. While the backend currently implements only user creation and water tracking endpoints, the remaining endpoints are documented according to the API specification. Future enhancements should focus on implementing missing endpoints, adding authentication to all endpoints, rate limiting, pagination, and performance optimizations.