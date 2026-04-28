from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import sqlite3
import os
import sys
import datetime
import json
import csv
from io import StringIO
import logging
from logging.handlers import RotatingFileHandler

sys.path.insert(0, os.path.dirname(__file__))
from meal_engine import generate_meal_plan
from validation import (
    sanitize_string, validate_exercise_data, validate_user_profile
)
from backup import backup_database, list_backups, export_user_data as export_user_backup

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'nutricoach-dev-secret-key-change-in-production')
jwt = JWTManager(app)

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# ========== LOGGING CONFIGURATION ==========
def setup_logging():
    """Configure comprehensive logging system"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler with rotation (10MB max, keep 5 backups)
    file_handler = RotatingFileHandler(
        'logs/nutricoach.log',
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
    ))
    file_handler.setLevel(logging.INFO)
    
    # Error file handler (separate file for errors)
    error_handler = RotatingFileHandler(
        'logs/nutricoach_errors.log',
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    error_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
    ))
    error_handler.setLevel(logging.ERROR)
    
    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(error_handler)
    app.logger.setLevel(logging.INFO)
    
    # Console handler for development
    if app.debug:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(console_handler)
    
    app.logger.info('NutriCoach AI application starting...')

setup_logging()

# ========== HEALTH CHECK ==========
@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint for deployment monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'NutriCoach AI',
        'version': '2.0',
        'timestamp': datetime.datetime.now().isoformat()
    }), 200

# ========== ERROR HANDLING MIDDLEWARE ==========
@app.errorhandler(400)
def bad_request(error):
    app.logger.warning(f'Bad request: {request.url} - {error.description}')
    return jsonify({
        'error': 'Bad Request',
        'message': error.description or 'Invalid request'
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    app.logger.warning(f'Unauthorized access attempt: {request.url}')
    return jsonify({
        'error': 'Unauthorized',
        'message': 'Authentication required'
    }), 401

@app.errorhandler(403)
def forbidden(error):
    app.logger.warning(f'Forbidden access: {request.url}')
    return jsonify({
        'error': 'Forbidden',
        'message': 'You do not have permission to access this resource'
    }), 403

@app.errorhandler(404)
def not_found(error):
    app.logger.warning(f'Resource not found: {request.url}')
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found'
    }), 404

@app.errorhandler(429)
def rate_limit_exceeded(error):
    app.logger.warning(f'Rate limit exceeded: {request.url} from {request.remote_addr}')
    return jsonify({
        'error': 'Rate Limit Exceeded',
        'message': 'Too many requests. Please try again later.'
    }), 429

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Internal server error: {request.url} - {str(error)}')
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred. Please try again later.'
    }), 500

# Global exception handler
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f'Unhandled exception: {request.url} - {str(e)}', exc_info=True)
    # Pass through HTTP errors
    if isinstance(e, HTTPException):
        return jsonify({
            'error': e.name,
            'message': e.description
        }), e.code
    # Non-HTTP error
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500

# ========== REQUEST LOGGING MIDDLEWARE ==========
@app.before_request
def log_request():
    """Log all incoming requests"""
    app.logger.info(f'{request.method} {request.path} from {request.remote_addr}')

@app.after_request
def log_response(response):
    """Log response status"""
    app.logger.info(f'{request.method} {request.path} - {response.status_code}')
    return response

# Enable CORS only in development
if os.environ.get('FLASK_ENV') != 'production':
    CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

# ========== VALIDATION MODELS ==========

class RegisterModel(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    
    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

class LoginModel(BaseModel):
    email: EmailStr
    password: str

class MealLogModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    calories: float = Field(default=0, ge=0)
    protein: float = Field(default=0, ge=0)
    carbs: float = Field(default=0, ge=0)
    fats: float = Field(default=0, ge=0)
    meal_type: str = Field(default='snack')
    date: Optional[str] = None

class WeightLogModel(BaseModel):
    weight: float = Field(..., gt=0, lt=500)
    date: Optional[str] = None

class WaterLogModel(BaseModel):
    amount_ml: int = Field(default=250, ge=1, le=5000)
    date: Optional[str] = None

# ========== HELPER FUNCTIONS ==========

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ========== AUTH ==========

@app.route('/api/v1/auth/register', methods=['POST'])
@limiter.limit("10 per minute")
def register():
    try:
        data = RegisterModel(**request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    password_hash = generate_password_hash(data.password)
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
                    (data.name, data.email, password_hash))
        conn.commit()
        user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Email already registered'}), 409

    conn.close()
    token = create_access_token(identity=str(user_id))
    return jsonify({'token': token, 'user_id': user_id}), 201


@app.route('/api/v1/auth/login', methods=['POST'])
@limiter.limit("20 per minute")
def login():
    try:
        data = LoginModel(**request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, password_hash, name FROM users WHERE email = ?', (data.email,))
    user = cur.fetchone()
    conn.close()

    if not user or not check_password_hash(user['password_hash'], data.password):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_access_token(identity=str(user['id']))
    return jsonify({'token': token, 'user_id': user['id'], 'name': user['name']})


@app.route('/api/v1/auth/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, email, age, gender, height, weight, goals, activity_level, diet_type, allergies, medical_conditions, budget FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()
    conn.close()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({key: user[key] for key in user.keys()})


# ========== PROFILE ==========

@app.route('/api/v1/users/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.json

    errors = validate_user_profile(data)
    if errors:
        return jsonify({'error': 'Validation failed', 'details': errors}), 400

    fields = ['name', 'age', 'gender', 'height', 'weight', 'goals',
              'activity_level', 'diet_type', 'allergies', 'medical_conditions', 'budget']
    
    updates = {}
    for k in fields:
        if k in data:
            val = data[k]
            if val is None:
                updates[k] = None
            elif k in ['age', 'height', 'weight', 'budget']:
                updates[k] = val
            else:
                updates[k] = sanitize_string(str(val), 1000)

    if not updates:
        return jsonify({'error': 'No fields to update'}), 400

    set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
    values = list(updates.values()) + [user_id]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'UPDATE users SET {set_clause} WHERE id = ?', values)
    conn.commit()
    conn.close()

    return jsonify({'message': 'Profile updated successfully'})


@app.route('/api/v1/users/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, email, age, gender, height, weight, goals, activity_level, diet_type, allergies, medical_conditions, budget FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()
    conn.close()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({key: user[key] for key in user.keys()})


@app.route('/api/v1/users/change-password', methods=['PUT'])
@jwt_required()
@limiter.limit("10 per minute")
def change_password():
    user_id = get_jwt_identity()
    data = request.json
    
    if not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Current password and new password are required'}), 400
    
    if len(data['new_password']) < 6:
        return jsonify({'error': 'New password must be at least 6 characters long'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT password_hash FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()
    
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    # Verify current password
    if not check_password_hash(user['password_hash'], data['current_password']):
        conn.close()
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    # Update to new password
    new_password_hash = generate_password_hash(data['new_password'])
    cur.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_password_hash, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Password updated successfully'})


@app.route('/api/v1/users/export', methods=['GET'])
@jwt_required()
def export_user_data():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT id, name, email, age, gender, height, weight, goals, activity_level, diet_type, allergies, medical_conditions, budget, created_at FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    profile = {key: user[key] for key in user.keys()}

    cur.execute('SELECT bmi, bmr, tdee, daily_calories, target_calories, created_at, updated_at FROM health_profiles WHERE user_id = ?', (user_id,))
    health = cur.fetchone()
    health_profile = {key: health[key] for key in health.keys()} if health else None

    cur.execute('SELECT id, date, total_calories, created_at FROM meal_plans WHERE user_id = ? ORDER BY date DESC', (user_id,))
    meal_plans = []
    for plan_row in cur.fetchall():
        plan = {key: plan_row[key] for key in plan_row.keys()}
        cur.execute('SELECT name, calories, protein, carbs, fats, date, meal_type, is_logged, created_at FROM meals WHERE meal_plan_id = ?', (plan['id'],))
        plan['meals'] = [{key: m[key] for key in m.keys()} for m in cur.fetchall()]
        meal_plans.append(plan)

    cur.execute('SELECT weight, date, created_at FROM weight_logs WHERE user_id = ? ORDER BY date DESC', (user_id,))
    weight_logs = [{key: w[key] for key in w.keys()} for w in cur.fetchall()]

    cur.execute('SELECT name, calories, protein, carbs, fats, date, meal_type, is_logged, created_at FROM meals WHERE user_id = ? AND is_logged = 1 ORDER BY date DESC', (user_id,))
    logged_meals = [{key: m[key] for key in m.keys()} for m in cur.fetchall()]

    conn.close()

    export_data = {
        'exported_at': datetime.datetime.now().isoformat(),
        'profile': profile,
        'health_profile': health_profile,
        'meal_plans': meal_plans,
        'weight_logs': weight_logs,
        'logged_meals': logged_meals
    }

    return jsonify(export_data)


# ========== HEALTH CALCULATIONS ==========

@app.route('/api/v1/health/calculate', methods=['POST'])
@jwt_required()
def calculate_health():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT age, gender, height, weight, goals, activity_level FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()
    conn.close()

    if not user or not all([user['age'], user['gender'], user['height'], user['weight']]):
        return jsonify({'error': 'Complete profile required before health calculation'}), 400

    age = user['age']
    gender = user['gender'].lower()
    height_cm = user['height']
    weight_kg = user['weight']
    goal = (user['goals'] or '').lower()
    activity_level = (user['activity_level'] or 'sedentary').lower()

    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 1)

    if gender == 'female':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    bmr = round(bmr, 0)

    multipliers = {
        'sedentary': 1.2,
        'lightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725,
        'super active': 1.9
    }
    tdee = round(bmr * multipliers.get(activity_level, 1.2), 0)

    if 'loss' in goal:
        target_calories = tdee - 500
    elif 'gain' in goal:
        target_calories = tdee + 500
    else:
        target_calories = tdee

    target_calories = round(target_calories, 0)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id FROM health_profiles WHERE user_id = ?', (user_id,))
    existing = cur.fetchone()

    if existing:
        cur.execute('''
            UPDATE health_profiles
            SET bmi=?, bmr=?, tdee=?, daily_calories=?, target_calories=?, updated_at=CURRENT_TIMESTAMP
            WHERE user_id=?
        ''', (bmi, bmr, tdee, tdee, target_calories, user_id))
    else:
        cur.execute('''
            INSERT INTO health_profiles (user_id, bmi, bmr, tdee, daily_calories, target_calories)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, bmi, bmr, tdee, tdee, target_calories))

    conn.commit()
    conn.close()

    return jsonify({
        'bmi': bmi,
        'bmr': bmr,
        'tdee': tdee,
        'daily_calories': tdee,
        'target_calories': target_calories,
        'goal': goal
    })


@app.route('/api/v1/health/profile', methods=['GET'])
@jwt_required()
def get_health_profile():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM health_profiles WHERE user_id = ?', (user_id,))
    profile = cur.fetchone()
    conn.close()

    if not profile:
        return jsonify({'error': 'Health profile not found'}), 404

    return jsonify({key: profile[key] for key in profile.keys()})


# ========== MEAL PLANS ==========

@app.route('/api/v1/meal-plans/generate', methods=['POST'])
@jwt_required()
def generate_plan():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT diet_type, allergies, goals, medical_conditions, age, gender FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()
    cur.execute('SELECT target_calories FROM health_profiles WHERE user_id = ?', (user_id,))
    health = cur.fetchone()
    conn.close()

    if not user or not health:
        return jsonify({'error': 'Profile and health calculation required'}), 400

    target_calories = health['target_calories'] or 2000
    diet_type = user['diet_type'] or 'non-veg'
    allergies = (user['allergies'] or '').lower().split(',')
    goal = (user['goals'] or '').lower()
    medical_conditions = (user['medical_conditions'] or '').lower().split(',') if user['medical_conditions'] else []
    age = user['age']
    gender = user['gender']

    plan = generate_meal_plan(target_calories, diet_type, allergies, goal, medical_conditions, age, gender)

    conn = get_db_connection()
    cur = conn.cursor()
    today = datetime.date.today().isoformat()

    cur.execute('DELETE FROM meal_plans WHERE user_id = ? AND date = ?', (user_id, today))
    cur.execute('DELETE FROM meals WHERE user_id = ? AND date = ? AND meal_plan_id IS NOT NULL', (user_id, today))

    cur.execute('INSERT INTO meal_plans (user_id, date, total_calories) VALUES (?, ?, ?)',
                (user_id, today, plan['total_calories']))
    meal_plan_id = cur.lastrowid

    for meal in plan['meals']:
        cur.execute('''
            INSERT INTO meals (user_id, meal_plan_id, name, calories, protein, carbs, fats, date, meal_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, meal_plan_id, meal['name'], meal['calories'], meal['protein'],
              meal['carbs'], meal['fats'], today, meal['meal_type']))

    conn.commit()
    conn.close()

    return jsonify(plan)


@app.route('/api/v1/meal-plans/current', methods=['GET'])
@jwt_required()
def get_current_plan():
    user_id = get_jwt_identity()
    today = datetime.date.today().isoformat()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM meal_plans WHERE user_id = ? AND date = ?', (user_id, today))
    plan = cur.fetchone()

    if not plan:
        conn.close()
        return jsonify({'meals': [], 'total_calories': 0})

    cur.execute('SELECT name, calories, protein, carbs, fats, meal_type FROM meals WHERE meal_plan_id = ?', (plan['id'],))
    meals = [dict(row) for row in cur.fetchall()]
    conn.close()

    total = sum(m['calories'] for m in meals)
    return jsonify({'meals': meals, 'total_calories': total})


# ========== FOOD TRACKER ==========

@app.route('/api/v1/meals/log', methods=['POST'])
@jwt_required()
@limiter.limit("30 per minute")
def log_meal():
    try:
        data = MealLogModel(**request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    user_id = get_jwt_identity()
    date = data.date or datetime.date.today().isoformat()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO meals (user_id, name, calories, protein, carbs, fats, date, meal_type, is_logged)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
    ''', (user_id, data.name, data.calories, data.protein, data.carbs, data.fats, date, data.meal_type))
    conn.commit()
    meal_id = cur.lastrowid
    conn.close()

    return jsonify({'id': meal_id, 'message': 'Meal logged successfully'}), 201


@app.route('/api/v1/meals/today', methods=['GET'])
@jwt_required()
def get_today_meals():
    user_id = get_jwt_identity()
    today = datetime.date.today().isoformat()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT id, name, calories, protein, carbs, fats, meal_type, is_logged
        FROM meals WHERE user_id = ? AND date = ?
    ''', (user_id, today))
    meals = [dict(row) for row in cur.fetchall()]
    conn.close()

    total_calories = sum(m['calories'] for m in meals)
    return jsonify({'meals': meals, 'total_calories': total_calories})


@app.route('/api/v1/weight/log', methods=['POST'])
@jwt_required()
@limiter.limit("20 per minute")
def log_weight():
    try:
        data = WeightLogModel(**request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    user_id = get_jwt_identity()
    date = data.date or datetime.date.today().isoformat()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO weight_logs (user_id, weight, date) VALUES (?, ?, ?)',
                (user_id, data.weight, date))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Weight logged successfully'})


@app.route('/api/v1/weight/history', methods=['GET'])
@jwt_required()
def get_weight_history():
    user_id = get_jwt_identity()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT weight, date FROM weight_logs WHERE user_id = ? ORDER BY date ASC', (user_id,))
    history = [dict(row) for row in cur.fetchall()]
    conn.close()

    return jsonify({'history': history})


# ========== DASHBOARD SUMMARY ==========

@app.route('/api/v1/dashboard/summary', methods=['GET'])
@jwt_required()
def dashboard_summary():
    user_id = get_jwt_identity()
    today = datetime.date.today().isoformat()

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT name, weight, goals FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()

    cur.execute('SELECT bmi, bmr, target_calories FROM health_profiles WHERE user_id = ?', (user_id,))
    health = cur.fetchone()

    cur.execute('SELECT calories FROM meals WHERE user_id = ? AND date = ?', (user_id, today))
    meals = cur.fetchall()
    consumed = sum(m['calories'] for m in meals)

    cur.execute('SELECT weight, date FROM weight_logs WHERE user_id = ? ORDER BY date DESC LIMIT 1', (user_id,))
    latest_weight = cur.fetchone()

    cur.execute('SELECT weight FROM weight_logs WHERE user_id = ? ORDER BY date ASC LIMIT 1', (user_id,))
    start_weight = cur.fetchone()

    cur.execute('SELECT amount_ml FROM water_logs WHERE user_id = ? AND date = ?', (user_id, today))
    water_entries = cur.fetchall()
    water_intake = sum(w['amount_ml'] for w in water_entries)

    conn.close()

    target = health['target_calories'] if health else 2000
    goal_progress = 0
    if start_weight and latest_weight and start_weight['weight']:
        diff = abs(latest_weight['weight'] - start_weight['weight'])
        goal_progress = min(round((diff / start_weight['weight']) * 100, 1), 100)

    return jsonify({
        'name': user['name'] if user else None,
        'goal': user['goals'] if user else None,
        'bmi': health['bmi'] if health else None,
        'bmr': health['bmr'] if health else None,
        'target_calories': target,
        'consumed_calories': consumed,
        'remaining_calories': round(target - consumed, 0),
        'latest_weight': latest_weight['weight'] if latest_weight else None,
        'goal_progress_percent': goal_progress,
        'water_intake': water_intake
    })


# ========== WATER INTAKE ==========

@app.route('/api/v1/water/log', methods=['POST'])
@jwt_required()
@limiter.limit("30 per minute")
def log_water():
    try:
        data = WaterLogModel(**request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    user_id = get_jwt_identity()
    date = data.date or datetime.date.today().isoformat()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO water_logs (user_id, amount_ml, date) VALUES (?, ?, ?)',
                (user_id, data.amount_ml, date))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Water logged'}), 201


@app.route('/api/v1/water/today', methods=['GET'])
@jwt_required()
def get_water_today():
    user_id = get_jwt_identity()
    today = datetime.date.today().isoformat()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT amount_ml FROM water_logs WHERE user_id= ? AND date = ?', (user_id, today))
    entries = cur.fetchall()
    conn.close()
    total = sum(e['amount_ml'] for e in entries)
    return jsonify({'total_ml': total, 'entries': len(entries)})


# ========== WEEKLY CHALLENGES ==========

@app.route('/api/v1/challenges/current', methods=['GET'])
@jwt_required()
def get_current_challenge():
    user_id = get_jwt_identity()
    today = datetime.date.today()
    week_start = (today - datetime.timedelta(days=today.weekday())).isoformat()
    week_end = (today + datetime.timedelta(days=6-today.weekday())).isoformat()
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get current week challenge
    cur.execute('''
        SELECT * FROM weekly_challenges 
        WHERE user_id = ? AND week_start_date = ?
    ''', (user_id, week_start))
    challenge = cur.fetchone()
    
    if not challenge:
        # Create default challenge for the week
        default_challenges = [
            {
                'title': '5 a Day Challenge',
                'description': 'Eat 5 servings of fruits & vegetables daily',
                'icon': '&#129367;',
                'goal': 35,
                'unit': 'servings'
            },
            {
                'title': 'Hydration Hero',
                'description': 'Drink 8 glasses of water every day',
                'icon': '&#128167;',
                'goal': 56,
                'unit': 'glasses'
            },
            {
                'title': 'Protein Power',
                'description': 'Reach your daily protein goal 5 days this week',
                'icon': '&#129385;',
                'goal': 5,
                'unit': 'days'
            }
        ]
        
        import random
        challenge_data = random.choice(default_challenges)
        
        cur.execute('''
            INSERT INTO weekly_challenges 
            (user_id, title, description, icon, goal, unit, week_start_date, week_end_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, challenge_data['title'], challenge_data['description'], 
              challenge_data['icon'], challenge_data['goal'], challenge_data['unit'],
              week_start, week_end))
        conn.commit()
        
        cur.execute('''
            SELECT * FROM weekly_challenges 
            WHERE user_id = ? AND week_start_date = ?
        ''', (user_id, week_start))
        challenge = cur.fetchone()
    
    conn.close()
    
    progress_percent = min((challenge['current_progress'] / challenge['goal']) * 100, 100)
    
    return jsonify({
        'id': challenge['id'],
        'title': challenge['title'],
        'description': challenge['description'],
        'icon': challenge['icon'],
        'goal': challenge['goal'],
        'unit': challenge['unit'],
        'current_progress': challenge['current_progress'],
        'progress_percent': round(progress_percent, 1),
        'week_start_date': challenge['week_start_date'],
        'week_end_date': challenge['week_end_date'],
        'is_completed': bool(challenge['is_completed'])
    })


@app.route('/api/v1/challenges/update', methods=['POST'])
@jwt_required()
def update_challenge_progress():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'progress' not in data:
        return jsonify({'error': 'Progress value is required'}), 400
    
    progress = data['progress']
    today = datetime.date.today()
    week_start = (today - datetime.timedelta(days=today.weekday())).isoformat()
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        UPDATE weekly_challenges 
        SET current_progress = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ? AND week_start_date = ?
    ''', (progress, user_id, week_start))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'progress': progress})


# ========== RECIPES ==========

@app.route('/api/v1/recipes', methods=['GET'])
@jwt_required()
def get_recipes():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    
    diet_type = request.args.get('diet_type')
    meal_type = request.args.get('meal_type')
    max_calories = request.args.get('max_calories')
    
    query = 'SELECT * FROM recipes WHERE 1=1'
    params = []
    
    if diet_type:
        query += ' AND diet_type = ?'
        params.append(diet_type)
    if meal_type:
        query += ' AND meal_type = ?'
        params.append(meal_type)
    if max_calories:
        query += ' AND calories <= ?'
        params.append(float(max_calories))
    
    query += ' ORDER BY name ASC'
    cur.execute(query, params)
    recipes = [{k: row[k] for k in row.keys()} for row in cur.fetchall()]
    conn.close()
    
    return jsonify({'recipes': recipes})


@app.route('/api/v1/recipes/<int:recipe_id>', methods=['GET'])
@jwt_required()
def get_recipe(recipe_id):
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,))
    recipe = cur.fetchone()
    conn.close()
    
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
    
    return jsonify({k: recipe[k] for k in recipe.keys()})


@app.route('/api/v1/recipes/suggestions', methods=['GET'])
@jwt_required()
def get_recipe_suggestions():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT diet_type, medical_conditions FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()
    
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    diet_type = user['diet_type'] or 'veg'
    query = 'SELECT * FROM recipes WHERE diet_type = ? OR diet_type = "vegan" ORDER BY RANDOM() LIMIT 20'
    cur.execute(query, (diet_type,))
    recipes = [{k: row[k] for k in row.keys()} for row in cur.fetchall()]
    conn.close()
    
    return jsonify({'recipes': recipes})


@app.route('/api/v1/recipes/<int:recipe_id>/favorite', methods=['POST'])
@jwt_required()
def toggle_recipe_favorite(recipe_id):
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT is_favorite FROM recipes WHERE id = ?', (recipe_id,))
    recipe = cur.fetchone()
    
    if not recipe:
        conn.close()
        return jsonify({'error': 'Recipe not found'}), 404
    
    new_favorite = not recipe['is_favorite']
    cur.execute('UPDATE recipes SET is_favorite = ? WHERE id = ?', (new_favorite, recipe_id))
    conn.commit()
    conn.close()
    
    return jsonify({'is_favorite': new_favorite})


# ========== BODY MEASUREMENTS ==========

@app.route('/api/v1/measurements/log', methods=['POST'])
@jwt_required()
def log_measurement():
    user_id = get_jwt_identity()
    data = request.json
    date = data.get('date', datetime.date.today().isoformat())
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO body_measurements (user_id, date, body_fat, waist, hips, chest, left_arm, right_arm, left_thigh, right_thigh, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (user_id, date, data.get('body_fat'), data.get('waist'), data.get('hips'), data.get('chest'),
         data.get('left_arm'), data.get('right_arm'), data.get('left_thigh'), data.get('right_thigh'), data.get('notes'))
    )
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Measurement logged successfully'}), 201


@app.route('/api/v1/measurements/history', methods=['GET'])
@jwt_required()
def get_measurements_history():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM body_measurements WHERE user_id = ? ORDER BY date DESC', (user_id,))
    measurements = [{k: row[k] for k in row.keys()} for row in cur.fetchall()]
    conn.close()
    
    return jsonify({'measurements': measurements})


# ========== EXERCISE LOGS ==========

# Exercise calorie database (calories per minute by intensity)
EXERCISE_CALORIE_DB = {
    'running': {'low': 8.0, 'moderate': 11.5, 'high': 15.0, 'very high': 18.0},
    'walking': {'low': 3.0, 'moderate': 4.5, 'high': 6.0, 'very high': 7.5},
    'cycling': {'low': 6.0, 'moderate': 8.5, 'high': 11.0, 'very high': 14.0},
    'swimming': {'low': 7.0, 'moderate': 9.5, 'high': 12.0, 'very high': 15.0},
    'weight training': {'low': 4.0, 'moderate': 6.0, 'high': 8.0, 'very high': 10.0},
    'yoga': {'low': 2.5, 'moderate': 3.5, 'high': 4.5, 'very high': 5.5},
    'hiit': {'low': 8.5, 'moderate': 12.0, 'high': 15.5, 'very high': 19.0},
    'jump rope': {'low': 8.0, 'moderate': 11.0, 'high': 14.0, 'very high': 17.0},
    'push-ups': {'low': 5.0, 'moderate': 7.0, 'high': 9.0, 'very high': 11.0},
    'squats': {'low': 4.5, 'moderate': 6.5, 'high': 8.5, 'very high': 10.5},
    'plank': {'low': 3.0, 'moderate': 4.0, 'high': 5.0, 'very high': 6.0},
    'burpees': {'low': 8.5, 'moderate': 12.0, 'high': 15.5, 'very high': 19.0},
    'lunges': {'low': 4.5, 'moderate': 6.0, 'high': 7.5, 'very high': 9.0},
    'pull-ups': {'low': 5.5, 'moderate': 7.5, 'high': 9.5, 'very high': 11.5},
    'dancing': {'low': 5.0, 'moderate': 7.0, 'high': 9.0, 'very high': 11.0},
    'boxing': {'low': 7.0, 'moderate': 10.0, 'high': 13.0, 'very high': 16.0},
    'rowing': {'low': 6.5, 'moderate': 9.0, 'high': 11.5, 'very high': 14.0},
    'elliptical': {'low': 6.0, 'moderate': 8.0, 'high': 10.0, 'very high': 12.5},
    'stair climbing': {'low': 7.0, 'moderate': 9.5, 'high': 12.0, 'very high': 15.0},
    'pilates': {'low': 3.0, 'moderate': 4.5, 'high': 6.0, 'very high': 7.5},
}

def calculate_calories(exercise_name, duration_minutes, intensity='moderate'):
    """Auto-calculate calories burned based on exercise, duration, and intensity"""
    if not exercise_name or not duration_minutes:
        return 0
    
    exercise_lower = exercise_name.lower()
    intensity_lower = intensity.lower() if intensity else 'moderate'
    
    # Find matching exercise in database
    for key, rates in EXERCISE_CALORIE_DB.items():
        if key in exercise_lower or exercise_lower in key:
            rate = rates.get(intensity_lower, rates.get('moderate', 7.0))
            return round(rate * duration_minutes)
    
    # Default calorie rate for unknown exercises
    default_rates = {'low': 5.0, 'moderate': 7.0, 'high': 9.0, 'very high': 11.0}
    rate = default_rates.get(intensity_lower, 7.0)
    return round(rate * duration_minutes)


@app.route('/api/v1/exercise/log', methods=['POST'])
@jwt_required()
@limiter.limit("30 per hour")
def log_exercise():
    user_id = get_jwt_identity()
    data = request.json
    
    # Validate input
    errors = validate_exercise_data(data)
    if errors:
        app.logger.warning(f'Exercise validation failed for user {user_id}: {errors}')
        return jsonify({'error': 'Validation failed', 'details': errors}), 400
    
    date = data.get('date', datetime.date.today().isoformat())
    
    # Auto-calculate calories if not provided or if auto-calculation is preferred
    duration = data.get('duration_minutes')
    intensity = data.get('intensity', 'moderate')
    exercise_name = sanitize_string(data.get('exercise_name', ''), max_length=100)
    notes = sanitize_string(data.get('notes', ''), max_length=500)
    
    # Use provided calories or auto-calculate
    calories = data.get('calories_burned')
    if calories is None or calories == 0:
        calories = calculate_calories(exercise_name, duration, intensity)
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO exercise_logs (user_id, date, exercise_name, duration_minutes, calories_burned, intensity, notes) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (user_id, date, exercise_name, duration, calories, intensity, notes)
    )
    conn.commit()
    conn.close()
    
    app.logger.info(f'Exercise logged: user={user_id}, exercise={exercise_name}, duration={duration}min, calories={calories}')
    
    return jsonify({
        'message': 'Exercise logged successfully',
        'calories_calculated': calories
    }), 201


@app.route('/api/v1/exercise/history', methods=['GET'])
@jwt_required()
def get_exercise_history():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM exercise_logs WHERE user_id = ? ORDER BY date DESC', (user_id,))
    exercises = [{k: row[k] for k in row.keys()} for row in cur.fetchall()]
    conn.close()
    
    return jsonify({'exercises': exercises})


@app.route('/api/v1/exercise/today', methods=['GET'])
@jwt_required()
def get_today_exercise():
    user_id = get_jwt_identity()
    today = datetime.date.today().isoformat()
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM exercise_logs WHERE user_id = ? AND date = ?', (user_id, today))
    exercises = [{k: row[k] for k in row.keys()} for row in cur.fetchall()]
    total_calories = sum(e['calories_burned'] or 0 for e in exercises)
    total_duration = sum(e['duration_minutes'] or 0 for e in exercises)
    conn.close()
    
    return jsonify({
        'exercises': exercises,
        'total_calories_burned': total_calories,
        'total_duration_minutes': total_duration
    })


# ========== CUSTOM GOALS ==========

@app.route('/api/v1/users/goals', methods=['PUT'])
@jwt_required()
def update_custom_goals():
    user_id = get_jwt_identity()
    data = request.json
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id FROM custom_goals WHERE user_id = ?', (user_id,))
    existing = cur.fetchone()
    
    if existing:
        cur.execute(
            'UPDATE custom_goals SET water_goal_ml = ?, calorie_goal = ?, protein_goal = ?, carbs_goal = ?, fats_goal = ? WHERE user_id = ?',
            (data.get('water_goal_ml', 2500), data.get('calorie_goal'), data.get('protein_goal'),
             data.get('carbs_goal'), data.get('fats_goal'), user_id)
        )
    else:
        cur.execute(
            'INSERT INTO custom_goals (user_id, water_goal_ml, calorie_goal, protein_goal, carbs_goal, fats_goal) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, data.get('water_goal_ml', 2500), data.get('calorie_goal'), data.get('protein_goal'),
             data.get('carbs_goal'), data.get('fats_goal'))
        )
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Goals updated successfully'})


@app.route('/api/v1/users/goals', methods=['GET'])
@jwt_required()
def get_custom_goals():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM custom_goals WHERE user_id = ?', (user_id,))
    goals = cur.fetchone()
    conn.close()
    
    if not goals:
        return jsonify({
            'water_goal_ml': 2500,
            'calorie_goal': None,
            'protein_goal': None,
            'carbs_goal': None,
            'fats_goal': None
        })
    
    return jsonify({k: goals[k] for k in goals.keys()})


# ========== MEAL PLAN EXPORT ==========

@app.route('/api/v1/meal-plans/export/csv', methods=['GET'])
@jwt_required()
def export_meal_plan_csv():
    user_id = get_jwt_identity()
    today = datetime.date.today().isoformat()
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM meal_plans WHERE user_id = ? AND date = ?', (user_id, today))
    plan = cur.fetchone()
    
    if not plan:
        conn.close()
        return jsonify({'error': 'No meal plan found for today'}), 404
    
    cur.execute('SELECT name, calories, protein, carbs, fats, meal_type FROM meals WHERE meal_plan_id = ? ORDER BY CASE meal_type WHEN "breakfast" THEN 1 WHEN "lunch" THEN 2 WHEN "dinner" THEN 3 WHEN "snack" THEN 4 END', (plan['id'],))
    meals = cur.fetchall()
    conn.close()
    
    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Meal Type', 'Name', 'Calories', 'Protein (g)', 'Carbs (g)', 'Fats (g)'])
    
    for meal in meals:
        writer.writerow([
            meal['meal_type'].capitalize(),
            meal['name'],
            round(meal['calories']),
            round(meal['protein']),
            round(meal['carbs']),
            round(meal['fats'])
        ])
    
    writer.writerow([])
    writer.writerow(['Total', '', round(plan['total_calories']), '', '', ''])
    
    # Create response
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=meal-plan-{today}.csv'
    
    return response


@app.route('/api/v1/meal-plans/export/json', methods=['GET'])
@jwt_required()
def export_meal_plan_json():
    user_id = get_jwt_identity()
    today = datetime.date.today().isoformat()
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM meal_plans WHERE user_id = ? AND date = ?', (user_id, today))
    plan = cur.fetchone()
    
    if not plan:
        conn.close()
        return jsonify({'error': 'No meal plan found for today'}), 404
    
    cur.execute('SELECT name, calories, protein, carbs, fats, meal_type FROM meals WHERE meal_plan_id = ?', (plan['id'],))
    meals = [{k: m[k] for k in m.keys()} for m in cur.fetchall()]
    conn.close()
    
    export_data = {
        'date': today,
        'total_calories': round(plan['total_calories']),
        'meals': meals,
        'exported_at': datetime.datetime.now().isoformat()
    }
    
    response = make_response(json.dumps(export_data, indent=2))
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Disposition'] = f'attachment; filename=meal-plan-{today}.json'
    
    return response


# ========== LEGACY ENDPOINT ==========

@app.route('/api/v1/users', methods=['POST'])
def create_user_legacy():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (name, email, password_hash, age, weight, height, goals) VALUES (?,?,?,?,?,?,?)',
                (data['name'], data['email'], generate_password_hash('password'), data.get('age'), data.get('weight'), data.get('height'), data.get('goals')))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return jsonify({'id': user_id}), 201


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue(path):
    if path.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')


# ========== BACKUP & MAINTENANCE ENDPOINTS ==========

@app.route('/api/v1/admin/backup', methods=['POST'])
@jwt_required()
def create_backup():
    """Create database backup (admin only)"""
    user_id = get_jwt_identity()
    
    # Check if user is admin (user_id = 1 is admin)
    if str(user_id) != '1':
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        backup_path = backup_database()
        app.logger.info(f'Database backup created by user {user_id}: {backup_path}')
        return jsonify({
            'message': 'Backup created successfully',
            'backup_path': backup_path
        })
    except Exception as e:
        app.logger.error(f'Backup failed: {str(e)}')
        return jsonify({'error': 'Backup failed', 'details': str(e)}), 500


@app.route('/api/v1/admin/backups', methods=['GET'])
@jwt_required()
def get_backups():
    """List all backups (admin only)"""
    user_id = get_jwt_identity()
    
    if str(user_id) != '1':
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        backups = list_backups()
        return jsonify({'backups': backups})
    except Exception as e:
        return jsonify({'error': 'Failed to list backups', 'details': str(e)}), 500


@app.route('/api/v1/users/export-full', methods=['GET'])
@jwt_required()
def export_full_user_data():
    """Export all user data as JSON"""
    user_id = get_jwt_identity()
    
    try:
        export_path = export_user_backup(user_id)
        app.logger.info(f'User data exported: user={user_id}')
        
        # Read and return the export file
        with open(export_path, 'r') as f:
            import json
            export_data = json.load(f)
        
        return jsonify(export_data)
    except Exception as e:
        app.logger.error(f'Export failed for user {user_id}: {str(e)}')
        return jsonify({'error': 'Export failed', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
