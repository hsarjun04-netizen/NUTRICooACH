"""
Input validation and sanitization utilities for NutriCoach AI
"""
import re
from html import escape


def sanitize_string(value, max_length=500):
    """Sanitize string input by escaping HTML and limiting length"""
    if not value:
        return value
    if not isinstance(value, str):
        return str(value)
    # Escape HTML to prevent XSS
    sanitized = escape(value.strip())
    # Limit length
    return sanitized[:max_length]


def sanitize_email(email):
    """Validate and sanitize email address"""
    if not email:
        return None
    email = email.strip().lower()
    # Basic email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return email
    return None


def validate_password(password):
    """Validate password strength"""
    if not password:
        return False, "Password is required"
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if len(password) > 128:
        return False, "Password must be less than 128 characters"
    return True, "Valid"


def validate_number(value, min_val=None, max_val=None, field_name="Value"):
    """Validate numeric input"""
    if value is None:
        return None, f"{field_name} is required"
    try:
        num = float(value)
        if min_val is not None and num < min_val:
            return None, f"{field_name} must be at least {min_val}"
        if max_val is not None and num > max_val:
            return None, f"{field_name} must be at most {max_val}"
        return num, None
    except (ValueError, TypeError):
        return None, f"{field_name} must be a valid number"


def validate_date(date_str):
    """Validate date format (YYYY-MM-DD)"""
    if not date_str:
        return None, "Date is required"
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, str(date_str)):
        return None, "Date must be in YYYY-MM-DD format"
    return str(date_str), None


def validate_exercise_data(data):
    """Validate exercise log input data"""
    errors = []
    
    # Exercise name
    if not data.get('exercise_name'):
        errors.append("Exercise name is required")
    elif len(data['exercise_name']) > 100:
        errors.append("Exercise name must be less than 100 characters")
    
    # Duration
    duration = data.get('duration_minutes')
    if duration is None:
        errors.append("Duration is required")
    else:
        try:
            duration = int(duration)
            if duration <= 0:
                errors.append("Duration must be greater than 0")
            elif duration > 1440:  # 24 hours max
                errors.append("Duration cannot exceed 24 hours (1440 minutes)")
        except (ValueError, TypeError):
            errors.append("Duration must be a valid number")
    
    # Intensity
    valid_intensities = ['low', 'moderate', 'high', 'very high']
    intensity = data.get('intensity', 'moderate')
    if intensity not in valid_intensities:
        errors.append(f"Intensity must be one of: {', '.join(valid_intensities)}")
    
    # Notes (optional)
    if data.get('notes') and len(data['notes']) > 500:
        errors.append("Notes must be less than 500 characters")
    
    return errors


def validate_meal_data(data):
    """Validate meal log input data"""
    errors = []
    
    # Meal name
    if not data.get('name'):
        errors.append("Meal name is required")
    elif len(data['name']) > 200:
        errors.append("Meal name must be less than 200 characters")
    
    # Calories
    calories = data.get('calories')
    if calories is not None:
        try:
            calories = float(calories)
            if calories < 0:
                errors.append("Calories cannot be negative")
            elif calories > 5000:
                errors.append("Calories seem too high (max 5000 per meal)")
        except (ValueError, TypeError):
            errors.append("Calories must be a valid number")
    
    # Macros
    for macro in ['protein', 'carbs', 'fats']:
        value = data.get(macro)
        if value is not None:
            try:
                value = float(value)
                if value < 0:
                    errors.append(f"{macro.capitalize()} cannot be negative")
                elif value > 500:
                    errors.append(f"{macro.capitalize()} seems too high (max 500g)")
            except (ValueError, TypeError):
                errors.append(f"{macro.capitalize()} must be a valid number")
    
    # Meal type
    valid_meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
    meal_type = data.get('meal_type')
    if meal_type and meal_type not in valid_meal_types:
        errors.append(f"Meal type must be one of: {', '.join(valid_meal_types)}")
    
    return errors


def validate_user_profile(data):
    """Validate user profile update data"""
    errors = []
    
    # Name
    if data.get('name'):
        if len(data['name']) > 100:
            errors.append("Name must be less than 100 characters")
        if not re.match(r'^[a-zA-Z\s\-\.]+$', data['name']):
            errors.append("Name can only contain letters, spaces, hyphens, and periods")
    
    # Age
    age = data.get('age')
    if age is not None:
        try:
            age = int(age)
            if age < 10 or age > 120:
                errors.append("Age must be between 10 and 120")
        except (ValueError, TypeError):
            errors.append("Age must be a valid number")
    
    # Height
    height = data.get('height')
    if height is not None:
        try:
            height = float(height)
            if height < 50 or height > 300:
                errors.append("Height must be between 50 and 300 cm")
        except (ValueError, TypeError):
            errors.append("Height must be a valid number")
    
    # Weight
    weight = data.get('weight')
    if weight is not None:
        try:
            weight = float(weight)
            if weight < 20 or weight > 500:
                errors.append("Weight must be between 20 and 500 kg")
        except (ValueError, TypeError):
            errors.append("Weight must be a valid number")
    
    return errors


def paginate_query(page=1, per_page=50, max_per_page=100):
    """Validate and sanitize pagination parameters"""
    try:
        page = max(1, int(page))
        per_page = min(max(int(per_page), 1), max_per_page)
        offset = (page - 1) * per_page
        return page, per_page, offset
    except (ValueError, TypeError):
        return 1, per_page, 0
