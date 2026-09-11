import asyncpg
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.schemas import Token, UserCreate
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.db.database import Database

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    try:
        query = """INSERT INTO users
            (username, password_hash)
            VALUES ($1, $2) RETURNING id"""
        result = await Database.fetch(query, user.username, hashed_password)
        return {
            "message": "Successfully registered",
            "user_id": result[0]["id"]
        }
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    query = "SELECT id, password_hash FROM users WHERE username = $1"
    result = await Database.fetch(query, form_data.username)

    if not result:
        raise HTTPException(
            status_code=400,
            detail="Username or password incorrect"
        )

    db_user = result[0]

    if not verify_password(form_data.password, db_user["password_hash"]):
        raise HTTPException(
            status_code=400,
            detail="Username or password incorrect"
        )

    token = create_access_token(db_user["id"])
    return {"access_token": token, "token_type": "bearer"}
