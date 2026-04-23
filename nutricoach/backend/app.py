from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(__file__))
from meal_engine import generate_meal_plan

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'nutricoach-dev-secret-key-change-in-production'
jwt = JWTManager(app)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ========== AUTH ==========

@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Name, email and password are required'}), 400

    password_hash = generate_password_hash(password)
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
                    (name, email, password_hash))
        conn.commit()
        user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Email already registered'}), 409

    conn.close()
    token = create_access_token(identity=str(user_id))
    return jsonify({'token': token, 'user_id': user_id}), 201


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, password_hash, name FROM users WHERE email = ?', (email,))
    user = cur.fetchone()
    conn.close()

    if not user or not check_password_hash(user['password_hash'], password):
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

    fields = ['name', 'age', 'gender', 'height', 'weight', 'goals',
              'activity_level', 'diet_type', 'allergies', 'medical_conditions', 'budget']
    updates = {k: data.get(k) for k in fields if k in data}

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


@app.route('/api/v1/users/export', methods=['GET'])
@jwt_required()
def export_user_data():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()

    # User profile
    cur.execute('SELECT id, name, email, age, gender, height, weight, goals, activity_level, diet_type, allergies, medical_conditions, budget, created_at FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    profile = {key: user[key] for key in user.keys()}

    # Health profile
    cur.execute('SELECT bmi, bmr, tdee, daily_calories, target_calories, created_at, updated_at FROM health_profiles WHERE user_id = ?', (user_id,))
    health = cur.fetchone()
    health_profile = {key: health[key] for key in health.keys()} if health else None

    # Meal plans with meals
    cur.execute('SELECT id, date, total_calories, created_at FROM meal_plans WHERE user_id = ? ORDER BY date DESC', (user_id,))
    meal_plans = []
    for plan_row in cur.fetchall():
        plan = {key: plan_row[key] for key in plan_row.keys()}
        cur.execute('SELECT name, calories, protein, carbs, fats, date, meal_type, is_logged, created_at FROM meals WHERE meal_plan_id = ?', (plan['id'],))
        plan['meals'] = [{key: m[key] for key in m.keys()} for m in cur.fetchall()]
        meal_plans.append(plan)

    # Weight logs
    cur.execute('SELECT weight, date, created_at FROM weight_logs WHERE user_id = ? ORDER BY date DESC', (user_id,))
    weight_logs = [{key: w[key] for key in w.keys()} for w in cur.fetchall()]

    # Logged meals (independent)
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

    # BMI
    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 1)

    # BMR (Mifflin-St Jeor)
    if gender == 'female':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    bmr = round(bmr, 0)

    # TDEE multipliers
    multipliers = {
        'sedentary': 1.2,
        'lightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725,
        'super active': 1.9
    }
    tdee = round(bmr * multipliers.get(activity_level, 1.2), 0)

    # Target calories based on goal
    if 'loss' in goal:
        target_calories = tdee - 500
    elif 'gain' in goal:
        target_calories = tdee + 500
    else:
        target_calories = tdee

    target_calories = round(target_calories, 0)

    # Save to health_profiles
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

    # Save plan to database
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
def log_meal():
    user_id = get_jwt_identity()
    data = request.json

    name = data.get('name')
    calories = data.get('calories', 0)
    protein = data.get('protein', 0)
    carbs = data.get('carbs', 0)
    fats = data.get('fats', 0)
    meal_type = data.get('meal_type', 'snack')
    date = data.get('date', datetime.date.today().isoformat())

    if not name:
        return jsonify({'error': 'Meal name is required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO meals (user_id, name, calories, protein, carbs, fats, date, meal_type, is_logged)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
    ''', (user_id, name, calories, protein, carbs, fats, date, meal_type))
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
def log_weight():
    user_id = get_jwt_identity()
    data = request.json
    weight = data.get('weight')

    if weight is None:
        return jsonify({'error': 'Weight is required'}), 400

    date = data.get('date', datetime.date.today().isoformat())

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO weight_logs (user_id, weight, date) VALUES (?, ?, ?)',
                (user_id, weight, date))
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

    # User info
    cur.execute('SELECT name, weight, goals FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()

    # Health profile
    cur.execute('SELECT bmi, bmr, target_calories FROM health_profiles WHERE user_id = ?', (user_id,))
    health = cur.fetchone()

    # Today's meals
    cur.execute('SELECT calories FROM meals WHERE user_id = ? AND date = ?', (user_id, today))
    meals = cur.fetchall()
    consumed = sum(m['calories'] for m in meals)

    # Weight history
    cur.execute('SELECT weight, date FROM weight_logs WHERE user_id = ? ORDER BY date DESC LIMIT 1', (user_id,))
    latest_weight = cur.fetchone()

    cur.execute('SELECT weight FROM weight_logs WHERE user_id = ? ORDER BY date ASC LIMIT 1', (user_id,))
    start_weight = cur.fetchone()

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
        'goal_progress_percent': goal_progress
    })


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
