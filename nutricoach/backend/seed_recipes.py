"""Seed data for recipes database"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

recipes = [
    # Breakfast Recipes
    {
        'name': 'Oatmeal with Berries',
        'description': 'Healthy oatmeal topped with fresh berries and honey',
        'calories': 350,
        'protein': 12,
        'carbs': 58,
        'fats': 8,
        'diet_type': 'vegan',
        'meal_type': 'breakfast',
        'ingredients': '1/2 cup Rolled oats, 1/4 cup Mixed berries, 1 cup Almond milk, 1 tbsp Honey, 1 tsp Chia seeds',
        'instructions': 'Cook oats with almond milk. Top with berries, drizzle honey, and sprinkle chia seeds.',
        'prep_time': 5,
        'cook_time': 10,
        'servings': 1,
        'medical_tags': 'heart-healthy,high-fiber',
        'is_favorite': 0
    },
    {
        'name': 'Vegetable Omelette',
        'description': 'Fluffy omelette packed with fresh vegetables',
        'calories': 280,
        'protein': 18,
        'carbs': 8,
        'fats': 20,
        'diet_type': 'veg',
        'meal_type': 'breakfast',
        'ingredients': '3 Eggs, 1/4 cup Bell peppers (diced), 2 Tomatoes (chopped), 1 cup Spinach, 1/4 cup Cheese (shredded), 1 tbsp Olive oil',
        'instructions': 'Beat eggs. Sauté vegetables. Pour eggs over vegetables, add cheese, fold and cook until set.',
        'prep_time': 10,
        'cook_time': 8,
        'servings': 1,
        'medical_tags': 'high-protein,low-carb',
        'is_favorite': 0
    },
    {
        'name': 'Greek Yogurt Parfait',
        'description': 'Layered yogurt with granola and fresh fruits',
        'calories': 320,
        'protein': 20,
        'carbs': 45,
        'fats': 8,
        'diet_type': 'veg',
        'meal_type': 'breakfast',
        'ingredients': '1 cup Greek yogurt, 1/4 cup Granola, 1/2 cup Mixed berries, 1 tbsp Honey, 2 tbsp Nuts (chopped)',
        'instructions': 'Layer yogurt, granola, and berries in a glass. Drizzle with honey and top with nuts.',
        'prep_time': 5,
        'cook_time': 0,
        'servings': 1,
        'medical_tags': 'high-protein,probiotic',
        'is_favorite': 0
    },
    {
        'name': 'Chicken Breakfast Burrito',
        'description': 'Protein-packed breakfast burrito with grilled chicken',
        'calories': 450,
        'protein': 35,
        'carbs': 42,
        'fats': 15,
        'diet_type': 'non-veg',
        'meal_type': 'breakfast',
        'ingredients': '1 Whole wheat tortilla, 100g Grilled chicken, 2 Eggs, 1/4 cup Black beans, 2 tbsp Salsa, 1/4 Avocado (sliced)',
        'instructions': 'Warm tortilla. Fill with scrambled eggs, chicken, beans, salsa, and avocado. Roll and serve.',
        'prep_time': 10,
        'cook_time': 15,
        'servings': 1,
        'medical_tags': 'high-protein',
        'is_favorite': 0
    },
    {
        'name': 'Smoothie Bowl',
        'description': 'Thick smoothie bowl topped with fruits and seeds',
        'calories': 380,
        'protein': 15,
        'carbs': 62,
        'fats': 10,
        'diet_type': 'vegan',
        'meal_type': 'breakfast',
        'ingredients': '1 Banana, 1/2 cup Berries, 1 cup Almond milk, 1/4 cup Granola, 2 tbsp Coconut flakes, 1 tbsp Chia seeds',
        'instructions': 'Blend banana, berries, and almond milk until thick. Pour into bowl and top with granola, coconut, and chia seeds.',
        'prep_time': 10,
        'cook_time': 0,
        'servings': 1,
        'medical_tags': 'antioxidant-rich,high-fiber',
        'is_favorite': 0
    },
    
    # Lunch Recipes
    {
        'name': 'Grilled Chicken Salad',
        'description': 'Fresh salad with grilled chicken breast and vinaigrette',
        'calories': 420,
        'protein': 35,
        'carbs': 18,
        'fats': 22,
        'diet_type': 'non-veg',
        'meal_type': 'lunch',
        'ingredients': '150g Chicken breast, 2 cups Mixed greens, 1/2 cup Cherry tomatoes, 1/2 Cucumber (sliced), 1 tbsp Olive oil, 1/2 Lemon (juiced)',
        'instructions': 'Grill chicken and slice. Toss greens with vegetables. Top with chicken and drizzle with lemon-olive oil dressing.',
        'prep_time': 15,
        'cook_time': 15,
        'servings': 1,
        'medical_tags': 'high-protein,low-carb',
        'is_favorite': 0
    },
    {
        'name': 'Quinoa Buddha Bowl',
        'description': 'Nutritious bowl with quinoa, vegetables, and tahini dressing',
        'calories': 480,
        'protein': 18,
        'carbs': 65,
        'fats': 16,
        'diet_type': 'vegan',
        'meal_type': 'lunch',
        'ingredients': '1/2 cup Quinoa, 1/2 cup Chickpeas, 1 Sweet potato (cubed), 2 cups Kale, 1/2 Avocado, 2 tbsp Tahini',
        'instructions': 'Cook quinoa. Roast sweet potato and chickpeas. Massage kale. Arrange in bowl and drizzle with tahini dressing.',
        'prep_time': 15,
        'cook_time': 25,
        'servings': 1,
        'medical_tags': 'high-fiber,plant-protein',
        'is_favorite': 0
    },
    {
        'name': 'Turkey Wrap',
        'description': 'Whole wheat wrap with turkey, vegetables, and hummus',
        'calories': 380,
        'protein': 28,
        'carbs': 42,
        'fats': 12,
        'diet_type': 'non-veg',
        'meal_type': 'lunch',
        'ingredients': '1 Whole wheat tortilla, 100g Turkey breast, 2 leaves Lettuce, 2 Tomatoes (sliced), 2 tbsp Hummus, 1/4 Cucumber (sliced)',
        'instructions': 'Spread hummus on tortilla. Layer turkey, lettuce, tomatoes, and cucumber. Roll tightly and slice.',
        'prep_time': 10,
        'cook_time': 0,
        'servings': 1,
        'medical_tags': 'high-protein,low-fat',
        'is_favorite': 0
    },
    {
        'name': 'Paneer Tikka Masala',
        'description': 'Spicy paneer curry with aromatic spices',
        'calories': 520,
        'protein': 25,
        'carbs': 35,
        'fats': 30,
        'diet_type': 'veg',
        'meal_type': 'lunch',
        'ingredients': '200g Paneer (cubed), 3 Tomatoes (pureed), 2 Onions (sliced), 1/4 cup Cream, 1 tsp Garam masala, 1/2 tsp Turmeric, 1 cup Rice',
        'instructions': 'Marinate and grill paneer. Cook spiced tomato-onion gravy. Add paneer and cream. Serve with rice.',
        'prep_time': 20,
        'cook_time': 30,
        'servings': 2,
        'medical_tags': 'high-protein',
        'is_favorite': 0
    },
    {
        'name': 'Salmon Rice Bowl',
        'description': 'Grilled salmon with brown rice and steamed vegetables',
        'calories': 550,
        'protein': 40,
        'carbs': 55,
        'fats': 18,
        'diet_type': 'non-veg',
        'meal_type': 'lunch',
        'ingredients': '150g Salmon fillet, 1/2 cup Brown rice, 1 cup Broccoli, 1 tbsp Soy sauce, 1 tsp Ginger (grated), 1 tsp Sesame seeds',
        'instructions': 'Cook brown rice. Grill salmon with ginger and soy sauce. Steam broccoli. Assemble bowl and sprinkle sesame seeds.',
        'prep_time': 15,
        'cook_time': 25,
        'servings': 1,
        'medical_tags': 'omega-3,high-protein',
        'is_favorite': 0
    },
    
    # Dinner Recipes
    {
        'name': 'Grilled Chicken with Vegetables',
        'description': 'Lean grilled chicken with roasted seasonal vegetables',
        'calories': 450,
        'protein': 42,
        'carbs': 28,
        'fats': 18,
        'diet_type': 'non-veg',
        'meal_type': 'dinner',
        'ingredients': '150g Chicken breast, 1 Zucchini (sliced), 2 Bell peppers (sliced), 1 tbsp Olive oil, 2 cloves Garlic, 1 tsp Mixed herbs',
        'instructions': 'Marinate chicken with herbs and garlic. Grill chicken and roast vegetables. Serve together.',
        'prep_time': 15,
        'cook_time': 25,
        'servings': 1,
        'medical_tags': 'high-protein,low-carb',
        'is_favorite': 0
    },
    {
        'name': 'Vegetable Stir Fry with Tofu',
        'description': 'Colorful vegetable stir fry with crispy tofu',
        'calories': 380,
        'protein': 22,
        'carbs': 35,
        'fats': 16,
        'diet_type': 'vegan',
        'meal_type': 'dinner',
        'ingredients': '150g Tofu (cubed), 1 cup Broccoli, 2 Carrots (sliced), 1/2 cup Snap peas, 2 tbsp Soy sauce, 1 tsp Ginger (minced), 1/2 cup Brown rice',
        'instructions': 'Press and cube tofu. Stir fry vegetables and tofu. Add soy sauce and ginger. Serve over brown rice.',
        'prep_time': 15,
        'cook_time': 15,
        'servings': 2,
        'medical_tags': 'plant-protein,low-fat',
        'is_favorite': 0
    },
    {
        'name': 'Fish Curry with Rice',
        'description': 'Traditional fish curry in coconut milk with steamed rice',
        'calories': 520,
        'protein': 38,
        'carbs': 48,
        'fats': 20,
        'diet_type': 'non-veg',
        'meal_type': 'dinner',
        'ingredients': '200g White fish, 1/2 cup Coconut milk, 2 Tomatoes (chopped), 10 Curry leaves, 1 tsp Mustard seeds, 1 cup Rice',
        'instructions': 'Temper mustard seeds and curry leaves. Cook tomatoes and coconut milk. Add fish and simmer. Serve with rice.',
        'prep_time': 15,
        'cook_time': 25,
        'servings': 2,
        'medical_tags': 'omega-3,high-protein',
        'is_favorite': 0
    },
    {
        'name': 'Lentil Dal with Roti',
        'description': 'Protein-rich lentil dal served with whole wheat roti',
        'calories': 420,
        'protein': 20,
        'carbs': 68,
        'fats': 8,
        'diet_type': 'vegan',
        'meal_type': 'dinner',
        'ingredients': '1 cup Yellow lentils, 2 Tomatoes (chopped), 1 Onion (sliced), 1 tsp Cumin, 1/2 tsp Turmeric, 1 cup Whole wheat flour (for 4 rotis)',
        'instructions': 'Cook lentils with spices. Prepare tempering with cumin. Make roti dough and cook on griddle. Serve dal with roti.',
        'prep_time': 15,
        'cook_time': 30,
        'servings': 3,
        'medical_tags': 'high-fiber,plant-protein',
        'is_favorite': 0
    },
    {
        'name': 'Egg Fried Rice',
        'description': 'Quick and easy fried rice with eggs and vegetables',
        'calories': 450,
        'protein': 18,
        'carbs': 62,
        'fats': 14,
        'diet_type': 'veg',
        'meal_type': 'dinner',
        'ingredients': '1 cup Rice (cooked), 2 Eggs, 1/4 cup Peas, 1 Carrot (diced), 2 tbsp Soy sauce, 2 Green onions (chopped), 1 tsp Sesame oil',
        'instructions': 'Scramble eggs. Stir fry vegetables. Add cooked rice and soy sauce. Toss with sesame oil and green onions.',
        'prep_time': 10,
        'cook_time': 15,
        'servings': 2,
        'medical_tags': 'quick-meal',
        'is_favorite': 0
    },
    
    # Snack Recipes
    {
        'name': 'Trail Mix',
        'description': 'Energy-boosting mix of nuts, seeds, and dried fruits',
        'calories': 250,
        'protein': 8,
        'carbs': 28,
        'fats': 14,
        'diet_type': 'vegan',
        'meal_type': 'snack',
        'ingredients': '1/4 cup Almonds, 1/4 cup Walnuts, 1/4 cup Cashews, 1/4 cup Dried cranberries, 2 tbsp Pumpkin seeds, 2 tbsp Dark chocolate chips',
        'instructions': 'Mix all ingredients together. Store in an airtight container. Portion into small bags.',
        'prep_time': 5,
        'cook_time': 0,
        'servings': 5,
        'medical_tags': 'heart-healthy,energy-boost',
        'is_favorite': 0
    },
    {
        'name': 'Hummus with Vegetables',
        'description': 'Creamy hummus served with fresh vegetable sticks',
        'calories': 180,
        'protein': 6,
        'carbs': 22,
        'fats': 8,
        'diet_type': 'vegan',
        'meal_type': 'snack',
        'ingredients': '1 cup Chickpeas (canned), 2 tbsp Tahini, 1 Lemon (juiced), 1 clove Garlic, 3 Carrots (cut into sticks), 1 Cucumber (cut into sticks), 2 Bell peppers (sliced)',
        'instructions': 'Blend chickpeas, tahini, lemon, and garlic until smooth. Cut vegetables into sticks. Serve hummus with veggie sticks.',
        'prep_time': 10,
        'cook_time': 0,
        'servings': 4,
        'medical_tags': 'plant-protein,low-calorie',
        'is_favorite': 0
    },
    {
        'name': 'Protein Energy Balls',
        'description': 'No-bake energy balls with protein powder and dates',
        'calories': 150,
        'protein': 10,
        'carbs': 18,
        'fats': 6,
        'diet_type': 'veg',
        'meal_type': 'snack',
        'ingredients': '1 cup Dates (pitted), 2 scoops Protein powder, 1/2 cup Oats, 2 tbsp Peanut butter, 1 tbsp Chia seeds, 2 tbsp Dark chocolate chips',
        'instructions': 'Blend dates and peanut butter. Mix with oats, protein powder, and chia seeds. Roll into balls. Chill for 30 minutes.',
        'prep_time': 15,
        'cook_time': 0,
        'servings': 12,
        'medical_tags': 'high-protein,pre-workout',
        'is_favorite': 0
    },
    {
        'name': 'Fruit Smoothie',
        'description': 'Refreshing fruit smoothie with yogurt and honey',
        'calories': 220,
        'protein': 12,
        'carbs': 38,
        'fats': 3,
        'diet_type': 'veg',
        'meal_type': 'snack',
        'ingredients': '1 Banana, 1/2 cup Mango (chunks), 1/2 cup Greek yogurt, 1 tbsp Honey, 1/2 cup Ice',
        'instructions': 'Add all ingredients to blender. Blend until smooth. Pour into glass and serve immediately.',
        'prep_time': 5,
        'cook_time': 0,
        'servings': 1,
        'medical_tags': 'vitamin-rich,probiotic',
        'is_favorite': 0
    },
    {
        'name': 'Roasted Chickpeas',
        'description': 'Crunchy roasted chickpeas with spices',
        'calories': 180,
        'protein': 10,
        'carbs': 28,
        'fats': 4,
        'diet_type': 'vegan',
        'meal_type': 'snack',
        'ingredients': '2 cups Chickpeas (canned), 1 tbsp Olive oil, 1 tsp Paprika, 1 tsp Cumin, 1/2 tsp Garlic powder, 1/2 tsp Salt',
        'instructions': 'Drain and dry chickpeas. Toss with oil and spices. Roast at 400°F for 20-25 minutes until crispy.',
        'prep_time': 5,
        'cook_time': 25,
        'servings': 4,
        'medical_tags': 'high-fiber,plant-protein',
        'is_favorite': 0
    }
]

def seed_recipes():
    """Insert recipe seed data into the database"""
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Check if recipes already exist
    cur.execute('SELECT COUNT(*) FROM recipes')
    count = cur.fetchone()[0]
    
    if count > 0:
        print(f"Database already has {count} recipes. Skipping seed.")
        conn.close()
        return
    
    # Insert recipes
    for recipe in recipes:
        cur.execute('''
            INSERT INTO recipes (
                name, description, calories, protein, carbs, fats,
                diet_type, meal_type, ingredients, instructions,
                prep_time, cook_time, servings, medical_tags, is_favorite
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            recipe['name'], recipe['description'], recipe['calories'],
            recipe['protein'], recipe['carbs'], recipe['fats'],
            recipe['diet_type'], recipe['meal_type'], recipe['ingredients'],
            recipe['instructions'], recipe['prep_time'], recipe['cook_time'],
            recipe['servings'], recipe['medical_tags'], recipe['is_favorite']
        ))
    
    conn.commit()
    print(f"Successfully seeded {len(recipes)} recipes!")
    conn.close()

if __name__ == '__main__':
    seed_recipes()
