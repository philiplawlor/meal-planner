from database_client import mongodb_client
from typing import Dict, Any
import datetime

def create_collections():
    """
    Create and set up the initial MongoDB collections with their schemas and indexes.
    """
    # Get the database
    db = mongodb_client.db

    # Drop existing collections if they exist
    if "meals" in db.list_collection_names():
        db.meals.drop()
    if "meal_plans" in db.list_collection_names():
        db.meal_plans.drop()
    if "ratings" in db.list_collection_names():
        db.ratings.drop()

    # 1. Meals Collection
    meals_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "description", "ingredients", "instructions", "prep_time", "cook_time", "servings"],
            "properties": {
                "name": {
                    "bsonType": "string",
                    "description": "Name of the meal"
                },
                "description": {
                    "bsonType": "string",
                    "description": "Brief description of the meal"
                },
                "ingredients": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "required": ["name", "amount", "unit"],
                        "properties": {
                            "name": {"bsonType": "string"},
                            "amount": {"bsonType": "double"},
                            "unit": {"bsonType": "string"}
                        }
                    }
                },
                "instructions": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "string"
                    }
                },
                "prep_time": {
                    "bsonType": "int",
                    "description": "Preparation time in minutes"
                },
                "cook_time": {
                    "bsonType": "int",
                    "description": "Cooking time in minutes"
                },
                "servings": {
                    "bsonType": "int",
                    "description": "Number of servings"
                },
                "difficulty": {
                    "bsonType": "string",
                    "enum": ["easy", "medium", "hard"],
                    "description": "Difficulty level of the meal"
                },
                "cuisine": {
                    "bsonType": "string",
                    "description": "Type of cuisine"
                },
                "dietary_info": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "string",
                        "enum": ["vegetarian", "vegan", "gluten_free", "dairy_free", "paleo", "keto"]
                    }
                },
                "created_at": {
                    "bsonType": "date",
                    "description": "Creation date of the meal"
                },
                "updated_at": {
                    "bsonType": "date",
                    "description": "Last update date of the meal"
                }
            }
        }
    }

    # Create meals collection with validation
    db.create_collection("meals", validator=meals_schema)
    
    # Create indexes for meals
    db.meals.create_index([("name", 1)], unique=True)
    db.meals.create_index([("cuisine", 1)])
    db.meals.create_index([("difficulty", 1)])
    db.meals.create_index([("dietary_info", 1)])

    # 2. Meal Plans Collection
    meal_plans_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["user_id", "week_start", "meals"],
            "properties": {
                "user_id": {
                    "bsonType": "string",
                    "description": "User ID who created the meal plan"
                },
                "week_start": {
                    "bsonType": "date",
                    "description": "Start date of the meal plan week"
                },
                "meals": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "required": ["day", "meal_type", "meal_id"],
                        "properties": {
                            "day": {"bsonType": "int"},
                            "meal_type": {"enum": ["breakfast", "lunch", "dinner", "snack"]},
                            "meal_id": {"bsonType": "objectId"},
                            "notes": {"bsonType": "string"}
                        }
                    }
                },
                "created_at": {
                    "bsonType": "date",
                    "description": "Creation date of the meal plan"
                },
                "updated_at": {
                    "bsonType": "date",
                    "description": "Last update date of the meal plan"
                }
            }
        }
    }

    # Create meal_plans collection with validation
    db.create_collection("meal_plans", validator=meal_plans_schema)
    
    # Create indexes for meal_plans
    db.meal_plans.create_index([("user_id", 1), ("week_start", 1)], unique=True)
    db.meal_plans.create_index([("week_start", 1)])

    # 3. Ratings Collection
    ratings_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["user_id", "meal_id", "rating_type", "score"],
            "properties": {
                "user_id": {
                    "bsonType": "string",
                    "description": "User ID who gave the rating"
                },
                "meal_id": {
                    "bsonType": "objectId",
                    "description": "ID of the meal being rated"
                },
                "rating_type": {
                    "bsonType": "string",
                    "enum": ["overall", "taste", "difficulty", "nutrition", "prep_time"],
                    "description": "Type of rating"
                },
                "score": {
                    "bsonType": "int",
                    "minimum": 1,
                    "maximum": 5
                },
                "comment": {"bsonType": "string"},
                "created_at": {
                    "bsonType": "date",
                    "description": "Date when the rating was created"
                }
            }
        }
    }

    # Create ratings collection with validation
    db.create_collection("ratings", validator=ratings_schema)
    
    # Create indexes for ratings
    db.ratings.create_index([("user_id", 1), ("meal_id", 1), ("rating_type", 1)], unique=True)

    print("Collections created successfully!")

if __name__ == "__main__":
    create_collections()
