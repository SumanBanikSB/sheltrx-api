# app/routes/user_routes.py
from ..dependencies import get_current_user
from fastapi import APIRouter, HTTPException, status, Depends
from pymongo import ReturnDocument
from typing import List
from bson import ObjectId
from app.models import UserModel
from app.schemas import UserCreate, UserResponse
from ..main import db
from ..utils import send_email

router = APIRouter()


@router.get("/secure-data")
async def get_secure_data(current_user: dict = Depends(get_current_user)):
    return {"message": "This is protected data", "user": current_user}

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    user_data = user.dict()
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    result = await db["users"].insert_one(user_data)
    created_user = await db["users"].find_one({"_id": result.inserted_id})

    # Send email to the newly created user's email
    await send_email(
        to=user.email,
        subject="Welcome!",
        body=f"Hello {user.name}, you have been added as a {user.role}."
    )

    return UserResponse(**created_user)

@router.get("/", response_model=List[UserResponse])
async def get_users():
    users = await db["users"].find().to_list(100)
    return [UserResponse(**user) for user in users]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse(**user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user: UserCreate):
    updated_user = await db["users"].find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": user.dict()},
        return_document=ReturnDocument.AFTER,
    )
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse(**updated_user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    result = await db["users"].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
