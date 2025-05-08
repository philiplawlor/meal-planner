import requests
from datetime import datetime
import json

def test_endpoints():
    """
    Test all FastAPI endpoints.
    """
    base_url = "http://localhost:8000"
    
    try:
        # Test get_meals
        print("\nTesting get_meals...")
        response = requests.get(f"{base_url}/meals", params={
            "cuisine": "Italian",
            "limit": 2
        })
        response.raise_for_status()
        meals = response.json()
        print(f"Found {len(meals)} Italian meals")
        
        # Test get_meal_by_id
        if meals:
            print("\nTesting get_meal_by_id...")
            meal_id = meals[0]["_id"]
            response = requests.get(f"{base_url}/meals/{meal_id}")
            response.raise_for_status()
            meal = response.json()
            print(f"Retrieved meal: {meal['name']}")

        # Test create_meal_plan
        print("\nTesting create_meal_plan...")
        current_date = datetime.now()
        meal_plan_data = {
            "user_id": "test_user",
            "week_start": current_date.isoformat(),
            "meals": [
                {
                    "day": 1,
                    "meal_type": "breakfast",
                    "meal_id": meals[0]["_id"] if meals else "",
                    "notes": "Test breakfast"
                }
            ]
        }
        response = requests.post(f"{base_url}/meal-plans", json=meal_plan_data)
        response.raise_for_status()
        meal_plan = response.json()
        print(f"Created meal plan with ID: {meal_plan['_id']}")

        # Test get_meal_plan
        print("\nTesting get_meal_plan...")
        response = requests.get(f"{base_url}/meal-plans/test_user/{current_date.isoformat()}")
        response.raise_for_status()
        retrieved_plan = response.json()
        print(f"Retrieved meal plan with {len(retrieved_plan['meals'])} meals")

        # Test create_rating
        print("\nTesting create_rating...")
        rating_data = {
            "user_id": "test_user",
            "meal_id": meals[0]["_id"] if meals else "",
            "rating_type": "overall",
            "score": 5,
            "comment": "Test rating",
            "created_at": datetime.now().isoformat()
        }
        response = requests.post(f"{base_url}/ratings", json=rating_data)
        response.raise_for_status()
        rating = response.json()
        print(f"Created rating with score: {rating['score']}")

    except requests.exceptions.RequestException as e:
        print(f"Error testing endpoints: {e}")

if __name__ == "__main__":
    test_endpoints()
