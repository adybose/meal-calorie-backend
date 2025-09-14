# meal-calorie-backend

This is the backend code for the Meal Calories Counter application that accepts a dish name and number of servings and
returns the total calorie count using the free USDA FoodData Central API.


## Application File Structure
```
meal-calorie-backend/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   └── calories.py
├── utils/
│   ├── auth.py
│   └── calories.py
├── .env.example
├── requirements.txt
└── .gitignore  # Includes: .env, __pycache__, venv/, etc.
```

## Local Development Setup
- Clone the repository to a desired location in your computer with:
```bash
git clone git@github.com:adybose/meal-calorie-backend.git
```
- Enter the repository root:
```bash
cd meal-calorie-backend
```
- Create a virtual environment to install all dependencies:
```bash
python3 -m venv mealenv
```
- Activate the Python virtual environment:
```bash
source mealenv/bin/activate
```
- Install/update the Python dependencies:
```bash
pip install -r requirements.txt
```
> **_NOTE:_**
The requirements are based on these main packages: fastapi, uvicorn, sqlalchemy, psycopg2-binary, python-dotenv, requests, fuzzywuzzy, python-levenshtein, passlib[bcrypt], python-jose[cryptography]


## Usage
Run the application with:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
