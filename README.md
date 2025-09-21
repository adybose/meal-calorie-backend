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
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_calories.py
│   ├── test_models.py
│   ├── test_utils_auth.py
│   └── test_utils_calories.py
├── .env.example
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
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
- Create a `.env` file based on the `.env.example`
- Add your USDA API key to the `USDA_API_KEY` environment variable
- Generate a secret key using this script and add it to the `SECRET_KEY` :
    ```python
    import secrets
    print(secrets.token_hex(32))
    ```


## Usage
Run the application with:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```


## Installation using Docker

### Prerequisites
- Docker and Docker Compose installed on your system.

### Setup
- Clone the repository as explained above

- Create and configure the `.env` file as explained  above
- Build and run the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

   This will start both the PostgreSQL database and the FastAPI backend application.

### Usage
- The application will be available at `http://localhost:8000`
- API documentation can be accessed at `http://localhost:8000/docs`
- The database data persists in a Docker volume named `postgres_data`


## Running Tests
Run the unit tests using pytest:
```bash
pytest
```

Or with verbose output:
```bash
pytest -v
```
