from fastapi import FastAPI

app = FastAPI(title="Meal Calorie Count Generator Backend")

@app.get("/")
def read_root():
    return {"message": "Meal Calorie Count Generator Backend is running"}