from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class CalorieRequest(BaseModel):
    dish_name: str
    servings: int

class CalorieResponse(BaseModel):
    dish_name: str
    servings: int
    calories_per_serving: float
    total_calories: float
    source: str = "USDA FoodData Central"

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
