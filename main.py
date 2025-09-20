from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, calories

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meal Calorie Count Generator Backend")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(calories.router)

@app.get("/")
def read_root():
    return {"message": "Meal Calorie Count Generator Backend is running"}
