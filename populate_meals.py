from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('DATABASE_NAME')]
collection = db['Foods']

# Clear existing data first
collection.delete_many({})

# Sample meals data
sample_meals = [
    {
        "name": "Spaghetti Carbonara",
        "description": "Classic Italian pasta dish with creamy sauce",
        "cuisine": "Italian",
        "difficulty": "medium",
        "dietary_info": ["gluten-free", "dairy-free"],
        "ingredients": [
            {"name": "spaghetti", "amount": 400.0, "unit": "g"},
            {"name": "pancetta", "amount": 100.0, "unit": "g"},
            {"name": "eggs", "amount": 4, "unit": ""},
            {"name": "parmesan", "amount": 100.0, "unit": "g"}
        ],
        "instructions": [
            "Cook spaghetti according to package instructions",
            "Fry pancetta until crispy",
            "Beat eggs with parmesan",
            "Combine all ingredients and serve"
        ],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "name": "Chicken Stir Fry",
        "description": "Quick and healthy stir fry dish",
        "cuisine": "Chinese",
        "difficulty": "easy",
        "dietary_info": ["low-carb"],
        "ingredients": [
            {"name": "chicken breast", "amount": 500.0, "unit": "g"},
            {"name": "broccoli", "amount": 200.0, "unit": "g"},
            {"name": "soy sauce", "amount": 2, "unit": "tbsp"},
            {"name": "garlic", "amount": 2, "unit": "cloves"}
        ],
        "instructions": [
            "Cut chicken into strips",
            "Stir fry chicken until cooked",
            "Add vegetables and soy sauce",
            "Serve with rice"
        ],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "name": "Classic American Burger",
        "description": "A classic American burger with all the fixings",
        "cuisine": "American",
        "difficulty": "easy",
        "dietary_info": ["beef", "dairy"],
        "ingredients": [
            {"name": "beef patty", "amount": 200.0, "unit": "g"},
            {"name": "bun", "amount": 1, "unit": ""},
            {"name": "cheddar cheese", "amount": 50.0, "unit": "g"},
            {"name": "lettuce", "amount": 1, "unit": "leaf"},
            {"name": "tomato", "amount": 1, "unit": ""},
            {"name": "onion", "amount": 1, "unit": "slice"},
            {"name": "ketchup", "amount": 1, "unit": "tbsp"},
            {"name": "mustard", "amount": 1, "unit": "tbsp"}
        ],
        "instructions": [
            "Cook beef patty to desired doneness",
            "Toast the bun",
            "Assemble burger with all ingredients",
            "Serve with fries"
        ],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

# Insert sample meals
print("Inserting sample meals...")
for meal in sample_meals:
    collection.insert_one(meal)
    print(f"Inserted meal: {meal['name']}")

print("\nData population complete!")
print(f"Total meals in collection: {collection.count_documents({})}")
