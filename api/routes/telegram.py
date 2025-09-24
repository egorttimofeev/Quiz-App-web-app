from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
import os
from models.schemas import User, UserCreate, Payment, PaymentCreate
from services.database import get_db

router = APIRouter()

@router.post("/webhook")
async def telegram_webhook(update: Dict[Any, Any], db=Depends(get_db)):
    """Webhook для обработки обновлений от Telegram"""
    try:
        # Обработка сообщений
        if "message" in update:
            message = update["message"]
            user_data = message["from"]
            
            # Создаем или получаем пользователя
            user_create = UserCreate(
                telegramId=str(user_data["id"]),
                username=user_data.get("username"),
                firstName=user_data.get("first_name"),
                lastName=user_data.get("last_name")
            )
            
            # Сохраняем пользователя в БД
            user = await create_or_get_user(user_create, db)
            
            return {"status": "ok", "user_id": user.id}
        
        # Обработка платежей
        elif "pre_checkout_query" in update:
            return await handle_pre_checkout(update["pre_checkout_query"], db)
        
        elif "message" in update and "successful_payment" in update["message"]:
            return await handle_successful_payment(update["message"], db)
        
        return {"status": "ok"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def create_or_get_user(user_data: UserCreate, db):
    """Создание или получение пользователя"""
    existing_user = await db.user.find_unique(
        where={"telegramId": user_data.telegramId}
    )
    
    if existing_user:
        return existing_user
    
    new_user = await db.user.create(
        data={
            "telegramId": user_data.telegramId,
            "username": user_data.username,
            "firstName": user_data.firstName,
            "lastName": user_data.lastName,
        }
    )
    return new_user

async def handle_pre_checkout(pre_checkout_query: Dict[Any, Any], db):
    """Обработка pre_checkout_query для платежа"""
    try:
        # Здесь можно добавить дополнительные проверки
        return {
            "method": "answerPreCheckoutQuery",
            "pre_checkout_query_id": pre_checkout_query["id"],
            "ok": True
        }
    except Exception as e:
        return {
            "method": "answerPreCheckoutQuery", 
            "pre_checkout_query_id": pre_checkout_query["id"],
            "ok": False,
            "error_message": str(e)
        }

async def handle_successful_payment(message: Dict[Any, Any], db):
    """Обработка успешного платежа"""
    try:
        payment_info = message["successful_payment"]
        user_id = message["from"]["id"]
        
        # Находим пользователя
        user = await db.user.find_unique(
            where={"telegramId": str(user_id)}
        )
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Сохраняем платеж
        payment = await db.payment.create(
            data={
                "userId": user.id,
                "telegramPaymentId": payment_info["telegram_payment_charge_id"],
                "amount": payment_info["total_amount"],
                "status": "completed"
            }
        )
        
        return {"status": "payment_processed", "payment_id": payment.id}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/payment/{user_id}/check")
async def check_user_payment(user_id: int, db=Depends(get_db)):
    """Проверка, может ли пользователь пересдать тест"""
    try:
        # Проверяем количество пройденных тестов
        test_count = await db.testresult.count(
            where={"userId": user_id}
        )
        
        if test_count == 0:
            return {"canRetake": True, "needPayment": False}
        
        # Проверяем, есть ли оплаченные пересдачи
        payments = await db.payment.find_many(
            where={
                "userId": user_id,
                "status": "completed"
            }
        )
        
        # Количество доступных пересдач = количество платежей
        available_retakes = len(payments)
        used_retakes = test_count - 1  # Первый тест бесплатный
        
        can_retake = available_retakes > used_retakes
        
        return {
            "canRetake": can_retake,
            "needPayment": not can_retake,
            "availableRetakes": available_retakes,
            "usedRetakes": max(0, used_retakes)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))