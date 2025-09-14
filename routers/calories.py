from fastapi import APIRouter, Depends, HTTPException
import requests
from sqlalchemy.orm import Session
from database import get_db
from schemas import CalorieRequest, CalorieResponse
from utils.calories import select_best_food
from auth import get_current_user
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="", tags=["calories"])
USDA_API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
USDA_API_KEY = os.getenv("USDA_API_KEY")

@router.post("/get-calories", response_model=CalorieResponse)
async def get_calories(request: CalorieRequest, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if request.servings <= 0:
        raise HTTPException(status_code=400, detail="Invalid servings: must be positive")

    params = {
        "query": request.dish_name,
        "api_key": USDA_API_KEY,
        "pageSize": 5
    }
    response = requests.get(USDA_API_URL, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="USDA API error")

    data = response.json()
    foods = data.get("foods", [])

    if not foods:
        raise HTTPException(status_code=404, detail="Dish not found")

    best_food = select_best_food(foods, request.dish_name)

    # Extract calories (nutrientId 1008 for energy kcal, usually per 100g)
    calories_per_100g = 0.0
    for nutrient in best_food.get("foodNutrients", []):
        if nutrient.get("nutrientId") == 1008:
            calories_per_100g = nutrient.get("value", 0.0)
            break

    # Assume 1 serving = 100g for simplicity; adjust if measureUnits has serving size
    calories_per_serving = calories_per_100g
    total_calories = calories_per_serving * request.servings

    return CalorieResponse(
        dish_name=request.dish_name,
        servings=request.servings,
        calories_per_serving=calories_per_serving,
        total_calories=total_calories
    )
