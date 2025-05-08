from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

app = FastAPI(
    title="Meal Planner API",
    description="API for managing meal plans and recipes",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data
MEALS = [
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
        ]
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
        ]
    }
]

@app.get("/")
async def root():
    return {"message": "Welcome to the Meal Planner API"}

@app.get("/meals")
async def get_meals():
    try:
        # Get unique values for filters
        cuisines = list(set(meal["cuisine"] for meal in MEALS))
        difficulties = list(set(meal["difficulty"] for meal in MEALS))
        dietary_info = list(set(info for meal in MEALS for info in meal["dietary_info"]))
        
        response_data = {
            "meals": MEALS,
            "filters": {
                "cuisines": cuisines,
                "difficulties": difficulties,
                "dietary_info": dietary_info
            }
        }
        
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
