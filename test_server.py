from fastmcp import MCPClient
from datetime import datetime, timezone
import json

# Create MCP client
mcp_client = MCPClient()

async def test_endpoints():
    """
    Test all MCP server endpoints.
    """
    try:
        # Test get_meals
        print("\nTesting get_meals...")
        meals = await mcp_client.call("get_meals", {
            "cuisine": "Italian",
            "limit": 2
        })
        print(f"Found {len(meals)} Italian meals")
        
        # Test get_meal_by_id
        if meals:
            print("\nTesting get_meal_by_id...")
            meal = await mcp_client.call("get_meal_by_id", {
                "meal_id": meals[0]["_id"]
            })
            print(f"Retrieved meal: {meal['name']}")

        # Test create_meal_plan
        print("\nTesting create_meal_plan...")
        current_date = datetime.now(timezone.utc)
        meal_plan = await mcp_client.call("create_meal_plan", {
            "user_id": "test_user",
            "week_start": current_date,
            "meals": [
                {
                    "day": 1,
                    "meal_type": "breakfast",
                    "meal_id": meals[0]["_id"] if meals else "",
                    "notes": "Test breakfast"
                }
            ]
        })
        print(f"Created meal plan with ID: {meal_plan['_id']}")

        # Test get_meal_plan
        print("\nTesting get_meal_plan...")
        retrieved_plan = await mcp_client.call("get_meal_plan", {
            "user_id": "test_user",
            "week_start": current_date
        })
        print(f"Retrieved meal plan with {len(retrieved_plan['meals'])} meals")

        # Test create_rating
        print("\nTesting create_rating...")
        rating = await mcp_client.call("create_rating", {
            "user_id": "test_user",
            "meal_id": meals[0]["_id"] if meals else "",
            "rating_type": "overall",
            "score": 5,
            "comment": "Test rating"
        })
        print(f"Created rating with score: {rating['score']}")

    except Exception as e:
        print(f"Error testing endpoints: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_endpoints())
