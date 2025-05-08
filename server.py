from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from database_client import mongodb_client
import datetime

app = FastAPI(
    title="Meal Planner API",
    description="API for managing meal plans and recipes",
    version="1.0.0"
)

@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Welcome to the Meal Planner API",
        "version": "1.0.0",
        "endpoints": {
            "meals": {
                "GET /meals": "List meals with optional filters",
                "GET /meals/{meal_id}": "Get a specific meal"
            },
            "meal_plans": {
                "POST /meal-plans": "Create a new meal plan",
                "GET /meal-plans/{user_id}/{week_start}": "Get a meal plan",
                "PUT /meal-plans/{meal_plan_id}": "Update a meal plan"
            },
            "ratings": {
                "POST /ratings": "Create a new rating"
            }
        }
    }

class Meal(BaseModel):
    name: str
    description: str
    ingredients: List[dict]
    instructions: List[str]
    prep_time: int
    cook_time: int
    servings: int
    difficulty: str
    cuisine: str
    dietary_info: List[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime

class MealPlan(BaseModel):
    user_id: str
    week_start: datetime.datetime
    meals: List[dict]
    created_at: datetime.datetime
    updated_at: datetime.datetime

class Rating(BaseModel):
    user_id: str
    meal_id: str
    rating_type: str
    score: int
    comment: Optional[str] = None
    created_at: datetime.datetime

@app.get("/meals", response_model=List[Meal])
async def get_meals(
    cuisine: Optional[str] = None,
    difficulty: Optional[str] = None,
    dietary_info: Optional[List[str]] = None,
    limit: int = 10
):
    """
    Get a list of meals with optional filters.
    """
    db = mongodb_client.db
    query = {}
    
    if cuisine:
        query["cuisine"] = cuisine
    if difficulty:
        query["difficulty"] = difficulty
    if dietary_info:
        query["dietary_info"] = {"$in": dietary_info}
    
    meals = list(db.meals.find(query).limit(limit))
    return meals

@app.get("/meals/{meal_id}", response_model=Meal)
async def get_meal_by_id(meal_id: str):
    """
    Get a meal by its ID.
    """
    db = mongodb_client.db
    meal = db.meals.find_one({"_id": meal_id})
    if meal:
        return meal
    raise HTTPException(status_code=404, detail=f"Meal with ID {meal_id} not found")

@app.post("/meal-plans", response_model=MealPlan)
async def create_meal_plan(meal_plan: MealPlan):
    """
    Create a new meal plan.
    """
    db = mongodb_client.db
    
    # Validate meal IDs
    for meal in meal_plan.meals:
        if not db.meals.find_one({"_id": meal["meal_id"]}):
            raise HTTPException(status_code=404, detail=f"Meal with ID {meal['meal_id']} not found")
    
    result = db.meal_plans.insert_one(meal_plan.dict())
    meal_plan.id = str(result.inserted_id)
    return meal_plan

@app.get("/meal-plans/{user_id}/{week_start}", response_model=MealPlan)
async def get_meal_plan(user_id: str, week_start: str):
    """
    Get a meal plan for a specific user and week.
    """
    db = mongodb_client.db
    meal_plan = db.meal_plans.find_one({
        "user_id": user_id,
        "week_start": week_start
    })
    if meal_plan:
        return meal_plan
    raise HTTPException(status_code=404, detail="Meal plan not found")

@app.put("/meal-plans/{meal_plan_id}", response_model=MealPlan)
async def update_meal_plan(meal_plan_id: str, update_data: dict):
    """
    Update an existing meal plan.
    """
    db = mongodb_client.db
    
    # Validate meal IDs in updated meals
    if "meals" in update_data:
        for meal in update_data["meals"]:
            if not db.meals.find_one({"_id": meal["meal_id"]}):
                raise HTTPException(status_code=404, detail=f"Meal with ID {meal['meal_id']} not found")
    
    result = db.meal_plans.update_one(
        {"_id": meal_plan_id},
        {"$set": {
            **update_data,
            "updated_at": datetime.datetime.now(datetime.timezone.utc)
        }}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail=f"Meal plan with ID {meal_plan_id} not found")
    
    return db.meal_plans.find_one({"_id": meal_plan_id})

@app.post("/ratings", response_model=Rating)
async def create_rating(rating: Rating):
    """
    Create a new rating for a meal.
    """
    db = mongodb_client.db
    
    # Validate meal exists
    if not db.meals.find_one({"_id": rating.meal_id}):
        raise HTTPException(status_code=404, detail=f"Meal with ID {rating.meal_id} not found")
    
    # Check if rating already exists
    existing_rating = db.ratings.find_one({
        "user_id": rating.user_id,
        "meal_id": rating.meal_id,
        "rating_type": rating.rating_type
    })
    
    if existing_rating:
        raise HTTPException(status_code=400, detail="Rating already exists for this meal and type")
    
    result = db.ratings.insert_one(rating.dict())
    rating.id = str(result.inserted_id)
    return rating

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
