from database_client import mongodb_client
from datetime import datetime, timedelta
import random

def create_sample_data():
    """
    Create sample data for testing the meal planner application.
    """
    db = mongodb_client.db

    # Sample meals
    sample_meals = [
        {
            "name": "Spaghetti Carbonara",
            "description": "Classic Italian pasta dish with creamy sauce",
            "ingredients": [
                {"name": "spaghetti", "amount": 400.0, "unit": "g"},
                {"name": "pancetta", "amount": 100.0, "unit": "g"},
                {"name": "eggs", "amount": 4.0, "unit": "pieces"},
                {"name": "parmesan", "amount": 100.0, "unit": "g"},
                {"name": "garlic", "amount": 2.0, "unit": "cloves"}
            ],
            "instructions": [
                "Cook spaghetti according to package instructions.",
                "Fry pancetta until crispy.",
                "Mix eggs and parmesan in a bowl.",
                "Combine all ingredients and serve hot."
            ],
            "prep_time": 15,
            "cook_time": 25,
            "servings": 4,
            "difficulty": "medium",
            "cuisine": "Italian",
            "dietary_info": ["gluten_free"],
            "created_at": datetime.now(datetime.UTC),
            "updated_at": datetime.now(datetime.UTC)
        },
        {
            "name": "Chicken Stir Fry",
            "description": "Quick and healthy stir fry with chicken and vegetables",
            "ingredients": [
                {"name": "chicken breast", "amount": 500.0, "unit": "g"},
                {"name": "broccoli", "amount": 200.0, "unit": "g"},
                {"name": "bell peppers", "amount": 2.0, "unit": "pieces"},
                {"name": "soy sauce", "amount": 50.0, "unit": "ml"},
                {"name": "garlic", "amount": 2.0, "unit": "cloves"}
            ],
            "instructions": [
                "Cut chicken into small pieces.",
                "Stir fry chicken until cooked.",
                "Add vegetables and cook for 5 minutes.",
                "Add sauce and serve with rice."
            ],
            "prep_time": 10,
            "cook_time": 20,
            "servings": 4,
            "difficulty": "easy",
            "cuisine": "Asian",
            "dietary_info": [],
            "created_at": datetime.now(datetime.UTC),
            "updated_at": datetime.now(datetime.UTC)
        },
        {
            "name": "Veggie Burger",
            "description": "Delicious vegetarian burger with quinoa and black beans",
            "ingredients": [
                {"name": "quinoa", "amount": 200.0, "unit": "g"},
                {"name": "black beans", "amount": 200.0, "unit": "g"},
                {"name": "onion", "amount": 1.0, "unit": "piece"},
                {"name": "garlic", "amount": 2.0, "unit": "cloves"},
                {"name": "breadcrumbs", "amount": 50.0, "unit": "g"}
            ],
            "instructions": [
                "Cook quinoa and black beans.",
                "Mix all ingredients in a bowl.",
                "Form into patties and cook on a pan.",
                "Serve with buns and toppings."
            ],
            "prep_time": 20,
            "cook_time": 15,
            "servings": 4,
            "difficulty": "easy",
            "cuisine": "American",
            "dietary_info": ["vegetarian", "vegan"],
            "created_at": datetime.now(datetime.UTC),
            "updated_at": datetime.now(datetime.UTC)
        }
    ]

    # Insert sample meals
    meal_ids = []
    for meal in sample_meals:
        result = db.meals.insert_one(meal)
        meal_ids.append(result.inserted_id)

    # Create sample meal plan
    current_date = datetime.now(datetime.UTC)
    sample_meal_plan = {
        "user_id": "user123",
        "week_start": current_date,
        "meals": [
            {
                "day": 1,
                "meal_type": "breakfast",
                "meal_id": meal_ids[0],
                "notes": "First meal of the week"
            },
            {
                "day": 2,
                "meal_type": "dinner",
                "meal_id": meal_ids[1],
                "notes": "Quick dinner option"
            },
            {
                "day": 3,
                "meal_type": "lunch",
                "meal_id": meal_ids[2],
                "notes": "Healthy lunch choice"
            }
        ],
        "created_at": datetime.now(datetime.UTC),
        "updated_at": datetime.now(datetime.UTC)
    }

    # Insert sample meal plan
    db.meal_plans.insert_one(sample_meal_plan)

    # Create sample ratings
    sample_ratings = [
        {
            "user_id": "user123",
            "meal_id": meal_ids[0],
            "rating_type": "overall",
            "score": 5,
            "comment": "Absolutely delicious!",
            "created_at": datetime.now(datetime.UTC)
        },
        {
            "user_id": "user123",
            "meal_id": meal_ids[1],
            "rating_type": "taste",
            "score": 4,
            "comment": "Very tasty, could use more sauce.",
            "created_at": datetime.now(datetime.UTC)
        }
    ]

    # Insert sample ratings
    for rating in sample_ratings:
        db.ratings.insert_one(rating)

    print("Sample data created successfully!")

if __name__ == "__main__":
    create_sample_data()
