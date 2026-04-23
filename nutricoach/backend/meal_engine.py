import random

# Indian food database with medical condition tags
# medical_tags: diabetic_friendly, low_sodium, low_fat, high_fiber, anti_inflammatory, high_protein
# warnings: high_sugar, high_sodium, high_fat, high_gi, fried
FOOD_DATABASE = [
    # Breakfast items
    {"name": "Idli (2 pcs)", "calories": 130, "protein": 4, "carbs": 26, "fats": 0.5, "type": "veg", "tags": ["breakfast", "south-indian"], "medical_tags": ["diabetic_friendly", "low_fat", "low_sodium"]},
    {"name": "Dosa with Chutney", "calories": 220, "protein": 5, "carbs": 30, "fats": 9, "type": "veg", "tags": ["breakfast", "south-indian"], "medical_tags": ["low_sodium"], "warnings": ["high_gi"]},
    {"name": "Masala Dosa", "calories": 300, "protein": 6, "carbs": 38, "fats": 14, "type": "veg", "tags": ["breakfast", "south-indian"], "medical_tags": [], "warnings": ["high_fat", "fried"]},
    {"name": "Upma", "calories": 200, "protein": 5, "carbs": 32, "fats": 6, "type": "veg", "tags": ["breakfast", "south-indian"], "medical_tags": ["low_fat"]},
    {"name": "Poha", "calories": 250, "protein": 5, "carbs": 40, "fats": 8, "type": "veg", "tags": ["breakfast"], "medical_tags": ["low_sodium"]},
    {"name": "Paratha with Curd", "calories": 300, "protein": 8, "carbs": 38, "fats": 13, "type": "veg", "tags": ["breakfast", "north-indian"], "medical_tags": [], "warnings": ["high_fat", "fried"]},
    {"name": "Aloo Paratha", "calories": 330, "protein": 7, "carbs": 42, "fats": 15, "type": "veg", "tags": ["breakfast", "north-indian"], "medical_tags": [], "warnings": ["high_fat", "fried", "high_gi"]},
    {"name": "Oats with Milk", "calories": 180, "protein": 8, "carbs": 28, "fats": 4, "type": "veg", "tags": ["breakfast"], "medical_tags": ["diabetic_friendly", "high_fiber", "low_fat", "low_sodium"]},
    {"name": "Egg Omelette (2 eggs)", "calories": 180, "protein": 14, "carbs": 2, "fats": 13, "type": "non-veg", "tags": ["breakfast"], "medical_tags": ["high_protein", "low_sodium"], "warnings": ["high_fat"]},
    {"name": "Egg Bhurji with Roti", "calories": 300, "protein": 16, "carbs": 32, "fats": 13, "type": "non-veg", "tags": ["breakfast"], "medical_tags": ["high_protein"]},
    {"name": "Paneer Bhurji", "calories": 250, "protein": 15, "carbs": 8, "fats": 18, "type": "veg", "tags": ["breakfast"], "medical_tags": ["high_protein", "anti_inflammatory"], "warnings": ["high_fat"]},
    {"name": "Sprouts Salad", "calories": 150, "protein": 8, "carbs": 22, "fats": 3, "type": "vegan", "tags": ["breakfast"], "medical_tags": ["diabetic_friendly", "high_fiber", "low_fat", "anti_inflammatory", "low_sodium"]},
    {"name": "Besan Chilla", "calories": 200, "protein": 8, "carbs": 24, "fats": 8, "type": "veg", "tags": ["breakfast"], "medical_tags": ["high_protein", "low_sodium"]},
    {"name": "Rava Uttapam", "calories": 230, "protein": 5, "carbs": 34, "fats": 8, "type": "veg", "tags": ["breakfast", "south-indian"], "medical_tags": ["low_sodium"]},
    {"name": "Daliya (Broken Wheat Porridge)", "calories": 170, "protein": 5, "carbs": 30, "fats": 3, "type": "veg", "tags": ["breakfast"], "medical_tags": ["diabetic_friendly", "high_fiber", "low_fat", "low_sodium"]},
    {"name": "Methi Thepla", "calories": 210, "protein": 6, "carbs": 28, "fats": 8, "type": "veg", "tags": ["breakfast", "north-indian"], "medical_tags": ["diabetic_friendly", "low_sodium", "anti_inflammatory"]},

    # Lunch items
    {"name": "Rice and Dal", "calories": 350, "protein": 12, "carbs": 60, "fats": 6, "type": "veg", "tags": ["lunch"], "medical_tags": ["low_fat", "low_sodium", "high_fiber"], "warnings": ["high_gi"]},
    {"name": "Rice and Sambar", "calories": 320, "protein": 10, "carbs": 55, "fats": 7, "type": "veg", "tags": ["lunch", "south-indian"], "medical_tags": ["low_fat", "anti_inflammatory"], "warnings": ["high_gi"]},
    {"name": "Roti with Dal", "calories": 300, "protein": 12, "carbs": 48, "fats": 7, "type": "veg", "tags": ["lunch", "north-indian"], "medical_tags": ["diabetic_friendly", "low_fat", "low_sodium", "high_fiber"]},
    {"name": "Roti with Sabzi", "calories": 280, "protein": 8, "carbs": 40, "fats": 10, "type": "veg", "tags": ["lunch", "north-indian"], "medical_tags": ["low_sodium", "high_fiber"]},
    {"name": "Roti with Paneer Curry", "calories": 380, "protein": 16, "carbs": 38, "fats": 18, "type": "veg", "tags": ["lunch", "north-indian"], "medical_tags": ["high_protein", "anti_inflammatory"], "warnings": ["high_fat"]},
    {"name": "Chicken Curry with Rice", "calories": 450, "protein": 30, "carbs": 50, "fats": 14, "type": "non-veg", "tags": ["lunch"], "medical_tags": ["high_protein", "anti_inflammatory"]},
    {"name": "Chicken Curry with Roti", "calories": 400, "protein": 30, "carbs": 35, "fats": 15, "type": "non-veg", "tags": ["lunch"], "medical_tags": ["high_protein", "anti_inflammatory"]},
    {"name": "Fish Curry with Rice", "calories": 380, "protein": 28, "carbs": 48, "fats": 10, "type": "non-veg", "tags": ["lunch"], "medical_tags": ["high_protein", "anti_inflammatory", "low_fat"]},
    {"name": "Rajma Chawal", "calories": 370, "protein": 14, "carbs": 58, "fats": 8, "type": "veg", "tags": ["lunch", "north-indian"], "medical_tags": ["high_fiber", "low_fat"], "warnings": ["high_gi"]},
    {"name": "Chole with Roti", "calories": 350, "protein": 14, "carbs": 48, "fats": 11, "type": "veg", "tags": ["lunch", "north-indian"], "medical_tags": ["high_fiber", "high_protein"]},
    {"name": "Veg Biryani", "calories": 350, "protein": 8, "carbs": 55, "fats": 10, "type": "veg", "tags": ["lunch"], "medical_tags": ["anti_inflammatory"], "warnings": ["high_sodium", "high_gi"]},
    {"name": "Chicken Biryani", "calories": 480, "protein": 32, "carbs": 52, "fats": 15, "type": "non-veg", "tags": ["lunch"], "medical_tags": ["high_protein"], "warnings": ["high_sodium", "high_gi"]},
    {"name": "Dal Makhani with Roti", "calories": 380, "protein": 13, "carbs": 42, "fats": 16, "type": "veg", "tags": ["lunch", "north-indian"], "medical_tags": ["high_fiber"], "warnings": ["high_fat"]},
    {"name": "Palak Paneer with Roti", "calories": 360, "protein": 16, "carbs": 35, "fats": 17, "type": "veg", "tags": ["lunch", "north-indian"], "medical_tags": ["high_protein", "anti_inflammatory"], "warnings": ["high_fat"]},
    {"name": "Curd Rice", "calories": 250, "protein": 8, "carbs": 42, "fats": 5, "type": "veg", "tags": ["lunch", "south-indian"], "medical_tags": ["low_fat", "probiotic"]},
    {"name": "Lemon Rice", "calories": 280, "protein": 5, "carbs": 48, "fats": 8, "type": "veg", "tags": ["lunch", "south-indian"], "medical_tags": ["low_fat"], "warnings": ["high_gi"]},
    {"name": "Brown Rice and Dal", "calories": 330, "protein": 12, "carbs": 52, "fats": 6, "type": "veg", "tags": ["lunch"], "medical_tags": ["diabetic_friendly", "high_fiber", "low_fat", "low_sodium"]},
    {"name": "Quinoa Pulao", "calories": 310, "protein": 10, "carbs": 45, "fats": 8, "type": "veg", "tags": ["lunch"], "medical_tags": ["diabetic_friendly", "high_fiber", "high_protein", "low_sodium"]},

    # Dinner items
    {"name": "Roti with Dal Tadka", "calories": 280, "protein": 12, "carbs": 42, "fats": 7, "type": "veg", "tags": ["dinner"], "medical_tags": ["low_fat", "low_sodium", "high_fiber"]},
    {"name": "Roti with Mix Veg", "calories": 260, "protein": 8, "carbs": 38, "fats": 9, "type": "veg", "tags": ["dinner"], "medical_tags": ["low_sodium", "high_fiber", "anti_inflammatory"]},
    {"name": "Khichdi", "calories": 250, "protein": 10, "carbs": 42, "fats": 5, "type": "veg", "tags": ["dinner"], "medical_tags": ["low_fat", "low_sodium", "easy_digest"]},
    {"name": "Grilled Chicken with Salad", "calories": 320, "protein": 35, "carbs": 10, "fats": 16, "type": "non-veg", "tags": ["dinner"], "medical_tags": ["high_protein", "low_sodium", "anti_inflammatory"], "warnings": ["high_fat"]},
    {"name": "Fish Tikka with Salad", "calories": 280, "protein": 30, "carbs": 8, "fats": 14, "type": "non-veg", "tags": ["dinner"], "medical_tags": ["high_protein", "low_sodium", "anti_inflammatory"], "warnings": ["high_fat"]},
    {"name": "Paneer Tikka", "calories": 260, "protein": 16, "carbs": 8, "fats": 18, "type": "veg", "tags": ["dinner"], "medical_tags": ["high_protein", "anti_inflammatory"], "warnings": ["high_fat"]},
    {"name": "Tandoori Chicken", "calories": 300, "protein": 32, "carbs": 4, "fats": 17, "type": "non-veg", "tags": ["dinner"], "medical_tags": ["high_protein", "low_sodium"], "warnings": ["high_fat"]},
    {"name": "Veg Soup with Roti", "calories": 200, "protein": 7, "carbs": 32, "fats": 4, "type": "veg", "tags": ["dinner"], "medical_tags": ["low_fat", "low_sodium", "high_fiber"]},
    {"name": "Chicken Soup", "calories": 180, "protein": 15, "carbs": 10, "fats": 8, "type": "non-veg", "tags": ["dinner"], "medical_tags": ["high_protein", "low_fat", "low_sodium"]},
    {"name": "Moong Dal with Roti", "calories": 260, "protein": 14, "carbs": 38, "fats": 5, "type": "veg", "tags": ["dinner"], "medical_tags": ["high_fiber", "low_fat", "low_sodium"]},
    {"name": "Bhindi Masala with Roti", "calories": 250, "protein": 7, "carbs": 34, "fats": 10, "type": "veg", "tags": ["dinner", "north-indian"], "medical_tags": ["low_sodium", "high_fiber", "anti_inflammatory"]},
    {"name": "Egg Curry with Roti", "calories": 350, "protein": 18, "carbs": 34, "fats": 16, "type": "non-veg", "tags": ["dinner"], "medical_tags": ["high_protein"]},
    {"name": "Stir-fried Vegetables with Tofu", "calories": 240, "protein": 14, "carbs": 20, "fats": 10, "type": "vegan", "tags": ["dinner"], "medical_tags": ["low_sodium", "high_fiber", "anti_inflammatory"]},

    # Snacks
    {"name": "Fruit Bowl", "calories": 100, "protein": 1, "carbs": 24, "fats": 0.5, "type": "vegan", "tags": ["snack"], "medical_tags": ["low_fat", "low_sodium", "anti_inflammatory"], "warnings": ["high_sugar"]},
    {"name": "Roasted Chana", "calories": 120, "protein": 7, "carbs": 18, "fats": 2, "type": "vegan", "tags": ["snack"], "medical_tags": ["diabetic_friendly", "high_fiber", "low_fat", "high_protein"]},
    {"name": "Handful of Nuts", "calories": 170, "protein": 5, "carbs": 6, "fats": 15, "type": "vegan", "tags": ["snack"], "medical_tags": ["diabetic_friendly", "anti_inflammatory"], "warnings": ["high_fat"]},
    {"name": "Sprouts Chaat", "calories": 130, "protein": 7, "carbs": 18, "fats": 3, "type": "vegan", "tags": ["snack"], "medical_tags": ["diabetic_friendly", "high_fiber", "low_fat", "anti_inflammatory"]},
    {"name": "Masala Buttermilk", "calories": 50, "protein": 3, "carbs": 5, "fats": 1, "type": "veg", "tags": ["snack"], "medical_tags": ["low_fat", "low_sodium", "probiotic"]},
    {"name": "Green Tea", "calories": 5, "protein": 0, "carbs": 1, "fats": 0, "type": "vegan", "tags": ["snack"], "medical_tags": ["diabetic_friendly", "anti_inflammatory", "low_sodium"]},
    {"name": "Boiled Eggs (2)", "calories": 140, "protein": 12, "carbs": 2, "fats": 10, "type": "non-veg", "tags": ["snack"], "medical_tags": ["high_protein", "low_sodium"], "warnings": ["high_fat"]},
    {"name": "Protein Shake", "calories": 150, "protein": 25, "carbs": 8, "fats": 2, "type": "veg", "tags": ["snack"], "medical_tags": ["high_protein", "low_fat", "low_sodium"]},
    {"name": "Dhokla", "calories": 160, "protein": 5, "carbs": 26, "fats": 4, "type": "veg", "tags": ["snack"], "medical_tags": ["low_fat", "low_sodium"]},
    {"name": "Makhana (Fox Nuts)", "calories": 100, "protein": 4, "carbs": 14, "fats": 3, "type": "veg", "tags": ["snack"], "medical_tags": ["diabetic_friendly", "low_fat", "low_sodium"]},
    {"name": "Cucumber and Carrot Sticks", "calories": 40, "protein": 1, "carbs": 8, "fats": 0, "type": "vegan", "tags": ["snack"], "medical_tags": ["diabetic_friendly", "high_fiber", "low_fat", "low_sodium", "anti_inflammatory"]},
    {"name": "Roasted Makhana", "calories": 120, "protein": 5, "carbs": 16, "fats": 4, "type": "veg", "tags": ["snack"], "medical_tags": ["diabetic_friendly", "low_sodium"]},
]


# Medical condition to preferred/warning tag mappings
MEDICAL_PREFERENCES = {
    "diabetes": {
        "prefer": ["diabetic_friendly", "high_fiber", "low_fat"],
        "avoid": ["high_sugar", "high_gi"]
    },
    "high bp": {
        "prefer": ["low_sodium", "high_fiber"],
        "avoid": ["high_sodium"]
    },
    "hypertension": {
        "prefer": ["low_sodium", "high_fiber"],
        "avoid": ["high_sodium"]
    },
    "high cholesterol": {
        "prefer": ["low_fat", "high_fiber"],
        "avoid": ["high_fat", "fried"]
    },
    "pcos": {
        "prefer": ["diabetic_friendly", "high_fiber", "anti_inflammatory", "high_protein"],
        "avoid": ["high_sugar", "high_gi", "fried"]
    },
    "thyroid": {
        "prefer": ["high_fiber", "anti_inflammatory"],
        "avoid": []
    },
    "obesity": {
        "prefer": ["high_fiber", "high_protein", "low_fat"],
        "avoid": ["high_fat", "fried", "high_sugar"]
    },
    "acid reflux": {
        "prefer": ["low_fat", "easy_digest"],
        "avoid": ["fried", "high_fat"]
    }
}


def filter_foods(diet_type, allergies, medical_conditions=None):
    """Filter food database based on diet type, allergies, and medical conditions."""
    if medical_conditions is None:
        medical_conditions = []

    allowed_types = {"veg": ["veg", "vegan"], "non-veg": ["veg", "vegan", "non-veg"], "vegan": ["vegan"]}
    type_filter = allowed_types.get(diet_type.lower(), ["veg", "vegan", "non-veg"])

    # Build medical prefer/avoid lists
    prefer_tags = set()
    avoid_tags = set()
    for condition in medical_conditions:
        condition = condition.strip().lower()
        mapping = MEDICAL_PREFERENCES.get(condition)
        if mapping:
            prefer_tags.update(mapping.get("prefer", []))
            avoid_tags.update(mapping.get("avoid", []))

    filtered = []
    for food in FOOD_DATABASE:
        if food["type"] not in type_filter:
            continue

        # Check allergies
        name_lower = food["name"].lower()
        skip = False
        for allergy in allergies:
            allergy = allergy.strip().lower()
            if not allergy:
                continue
            if allergy in name_lower:
                skip = True
                break
        if skip:
            continue

        # Check medical warnings
        food_warnings = set(food.get("warnings", []))
        if food_warnings & avoid_tags:
            continue

        filtered.append(food)

    return filtered, prefer_tags


def score_food_for_medical(food, prefer_tags):
    """Score a food higher if it matches medical preference tags."""
    if not prefer_tags:
        return 0
    food_medical = set(food.get("medical_tags", []))
    matches = food_medical & prefer_tags
    return len(matches)


def pick_meal(foods, meal_type, target_calories, prefer_tags=None):
    """Pick a meal from the food list matching the meal type and calorie target."""
    candidates = [f for f in foods if meal_type in f["tags"]]

    if not candidates:
        candidates = [f for f in foods if any(t in f["tags"] for t in ["lunch", "dinner"])]

    if not candidates:
        return None

    # Sort by: medical score (desc), then calorie closeness (asc)
    candidates.sort(key=lambda f: (-score_food_for_medical(f, prefer_tags), abs(f["calories"] - target_calories)))

    # Pick from top 3 for variety
    top = candidates[:min(3, len(candidates))]
    return random.choice(top)


def check_safety(target_calories, medical_conditions, age, gender):
    """Health safety layer: check for unsafe calorie targets and medical risks."""
    warnings = []

    if target_calories < 1200:
        warnings.append("Calorie target is very low. Please consult a doctor before following this plan.")
    elif target_calories < 1500:
        warnings.append("Calorie target is moderately low. Monitor your energy levels.")

    for condition in medical_conditions:
        condition = condition.strip().lower()
        if condition in ["diabetes", "high bp", "hypertension", "pcos", "thyroid"]:
            warnings.append(f"You have indicated {condition.title()}. This meal plan is tailored but not a substitute for professional medical advice.")

    if "diabetes" in [c.strip().lower() for c in medical_conditions]:
        if target_calories > 2500:
            warnings.append("High calorie target with diabetes. Ensure carbs are distributed evenly across meals.")

    return warnings


def generate_meal_plan(target_calories, diet_type="non-veg", allergies=None, goal="", medical_conditions=None, age=None, gender=None):
    """Generate a daily meal plan based on calorie target and preferences."""
    if allergies is None:
        allergies = []
    if medical_conditions is None:
        medical_conditions = []

    foods, prefer_tags = filter_foods(diet_type, allergies, medical_conditions)

    if not foods:
        foods, prefer_tags = filter_foods(diet_type, [], medical_conditions)

    # Adjust macro split based on goal
    goal_lower = (goal or "").lower()
    if "loss" in goal_lower:
        breakfast_pct = 0.25
        lunch_pct = 0.35
        dinner_pct = 0.30
        snack_pct = 0.10
    elif "gain" in goal_lower or "muscle" in goal_lower:
        breakfast_pct = 0.25
        lunch_pct = 0.30
        dinner_pct = 0.30
        snack_pct = 0.15
    else:
        breakfast_pct = 0.25
        lunch_pct = 0.35
        dinner_pct = 0.30
        snack_pct = 0.10

    # Medical-specific adjustments
    med_lower = [c.strip().lower() for c in medical_conditions]
    if "diabetes" in med_lower or "pcos" in med_lower:
        # More frequent smaller meals
        breakfast_pct = 0.22
        lunch_pct = 0.30
        dinner_pct = 0.28
        snack_pct = 0.20

    if "obesity" in med_lower:
        # Higher protein, spread meals
        breakfast_pct = 0.25
        lunch_pct = 0.30
        dinner_pct = 0.25
        snack_pct = 0.20

    # Calorie targets per meal
    breakfast_cal = target_calories * breakfast_pct
    lunch_cal = target_calories * lunch_pct
    dinner_cal = target_calories * dinner_pct
    snack_cal = target_calories * snack_pct

    breakfast = pick_meal(foods, "breakfast", breakfast_cal, prefer_tags)
    lunch = pick_meal(foods, "lunch", lunch_cal, prefer_tags)
    dinner = pick_meal(foods, "dinner", dinner_cal, prefer_tags)
    snack = pick_meal(foods, "snack", snack_cal, prefer_tags)

    meals = []
    for meal_type, meal_data in [("breakfast", breakfast), ("lunch", lunch), ("dinner", dinner), ("snack", snack)]:
        if meal_data:
            meals.append({
                "name": meal_data["name"],
                "calories": meal_data["calories"],
                "protein": meal_data["protein"],
                "carbs": meal_data["carbs"],
                "fats": meal_data["fats"],
                "meal_type": meal_type,
                "medical_tags": meal_data.get("medical_tags", []),
                "warnings": meal_data.get("warnings", [])
            })

    total_calories = sum(m["calories"] for m in meals)
    total_protein = sum(m["protein"] for m in meals)
    total_carbs = sum(m["carbs"] for m in meals)
    total_fats = sum(m["fats"] for m in meals)

    # Safety warnings
    safety_warnings = check_safety(target_calories, medical_conditions, age, gender)

    return {
        "meals": meals,
        "total_calories": total_calories,
        "total_protein": total_protein,
        "total_carbs": total_carbs,
        "total_fats": total_fats,
        "target_calories": target_calories,
        "diet_type": diet_type,
        "medical_conditions": medical_conditions,
        "safety_warnings": safety_warnings,
        "medical_notes": f"Plan tailored for: {', '.join(medical_conditions)}" if medical_conditions else "General wellness plan"
    }
