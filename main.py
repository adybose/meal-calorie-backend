from fastapi import FastAPI
from database import engine, Base
from routers import auth, calories

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meal Calorie Count Generator Backend")

app.include_router(auth.router)
app.include_router(calories.router)

@app.get("/")
def read_root():
    return {"message": "Meal Calorie Count Generator Backend is running"}
