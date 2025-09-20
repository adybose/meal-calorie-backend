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

@router.post("/get-calories")
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
    fdc_id = best_food['fdcId']

    # Fetch full details
    details_url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"
    details_params = {"api_key": USDA_API_KEY}
    details_response = requests.get(details_url, params=details_params)
    if details_response.status_code != 200:
        raise HTTPException(status_code=500, detail="USDA details API error")

    food_details = details_response.json()

    serving_size = food_details.get('servingSize', 100.0)
    serving_unit = food_details.get('servingSizeUnit', 'g')
    household_text = food_details.get('householdServingFullText', 'N/A')

    # Collect all nutrients per 100g
    per_100g_nutrients = []
    for nutrient in food_details.get('foodNutrients', []):
        nut_id = nutrient['nutrient']['id']
        nut_name = nutrient['nutrient']['name']
        nut_value = nutrient['amount']
        nut_unit = nutrient['nutrient']['unitName']
        # Handle energy kJ to kcal if needed
        if nut_id == 1008 and nut_unit == 'kJ':
            nut_value = round(nut_value / 4.184, 2)
            nut_unit = 'kcal'
        per_100g_nutrients.append({
            'id': nut_id,
            'name': nut_name,
            'value': nut_value,
            'unit': nut_unit
        })

    scale_factor_serving = serving_size / 100.0 if serving_unit == 'g' else 1.0
    per_serving_nutrients = [
        {
            'id': nut['id'],
            'name': nut['name'],
            'value': round(nut['value'] * scale_factor_serving, 2),
            'unit': nut['unit']
        }
        for nut in per_100g_nutrients
    ]

    total_servings = request.servings
    total_nutrients = [
        {
            'id': nut['id'],
            'name': nut['name'],
            'value': round(nut['value'] * total_servings, 2),
            'unit': nut['unit']
        }
        for nut in per_serving_nutrients
    ]

    return {
        'dish_name': request.dish_name,
        'selected_food': best_food.get('description', 'N/A'),
        'fdc_id': fdc_id,
        'serving_size': f"{serving_size} {serving_unit}",
        'household_serving_text': household_text,
        'total_servings': total_servings,
        'per_100g_nutrients': per_100g_nutrients,
        'per_serving_nutrients': per_serving_nutrients,
        'total_nutrients': total_nutrients
    }
