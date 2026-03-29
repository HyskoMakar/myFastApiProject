from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel, EmailStr

# models
class UserCreate(BaseModel):
    username: str
    email: EmailStr

# schemas
class User(BaseModel):
    id: int
    username: str
    email: EmailStr

app = FastAPI()

# db
users_db: List[User] = [
    User(id=1, username="ivan_petrov", email="ivan@example.com"),
    User(id=2, username="olena_u", email="olena@example.com"),
]

# routes
@app.get("/users", response_model=List[User])
def get_all_users():
    return users_db

@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: int):
    user = next((u for u in users_db if u.id == user_id), None)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/create_user", response_model=User)
def create_user(user_data: UserCreate):
    new_id = users_db[-1].id + 1 if users_db else 1
    
    new_user = User(
        id=new_id,
        username=user_data.username,
        email=user_data.email
    )
    
    users_db.append(new_user)
    return new_user