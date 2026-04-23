# API Endpoints and Data Models

## Base URL
`/api/v1`

## User Management
- **POST** `/users` - Create a new user
- **GET** `/users/{user_id}` - Retrieve user details
- **PUT** `/users/{user_id}` - Update user details
- **DELETE** `/users/{user_id}` - Delete a user

## Diet Preferences
- **POST** `/diet-preferences` - Set or update diet preferences for a user
- **GET** `/diet-preferences/{user_id}` - Get diet preferences for a user

## Meal Plans
- **POST** `/meal-plans` - Generate and save a personalized meal plan
- **GET** `/meal-plans/{user_id}` - Retrieve the latest meal plan for a user
- **GET** `/meal-plans/{user_id}/history` - Retrieve meal plan history

## Authentication
- **POST** `/auth/register` - Register a new user
- **POST** `/auth/login` - Authenticate and return a token

---

## Data Models

### User
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "age": "integer",
  "weight": "real",
  "height": "real",
  "goals": "string"
}
```

### DietPreference
```json
{
  "user_id": "integer",
  "allergies": "string",
  "dietary_restrictions": "string",
  "macronutrient_goals": "string"
}
```

### MealPlan
```json
{
  "id": "integer",
  "user_id": "integer",
  "date": "date",
  "meals": "string"
}