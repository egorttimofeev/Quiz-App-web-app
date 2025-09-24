from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.schemas import User, UserCreate
from services.database import get_db

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(user: UserCreate, db=Depends(get_db)):
    """Создание нового пользователя или получение существующего"""
    try:
        # Проверяем, существует ли пользователь
        existing_user = await db.user.find_unique(
            where={"telegramId": user.telegramId}
        )
        
        if existing_user:
            return existing_user
        
        # Создаем нового пользователя
        new_user = await db.user.create(
            data={
                "telegramId": user.telegramId,
                "username": user.username,
                "firstName": user.firstName,
                "lastName": user.lastName,
            }
        )
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{telegram_id}", response_model=User)
async def get_user(telegram_id: str, db=Depends(get_db)):
    """Получение пользователя по Telegram ID"""
    user = await db.user.find_unique(
        where={"telegramId": telegram_id}
    )
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/", response_model=List[User])
async def get_all_users(db=Depends(get_db)):
    """Получение всех пользователей"""
    users = await db.user.find_many()
    return users