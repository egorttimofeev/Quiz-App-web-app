from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.schemas import Question, QuestionCreate
from services.database import get_db
import random

router = APIRouter()

@router.post("/", response_model=Question)
async def create_question(question: QuestionCreate, db=Depends(get_db)):
    """Создание нового вопроса"""
    try:
        new_question = await db.question.create(
            data={
                "text": question.text,
                "option1": question.option1,
                "option2": question.option2,
                "option3": question.option3,
                "option4": question.option4,
                "correctAnswer": question.correctAnswer,
            }
        )
        return new_question
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/random", response_model=List[Question])
async def get_random_questions(db=Depends(get_db)):
    """Получение 10 случайных вопросов для теста"""
    try:
        # Получаем все вопросы
        all_questions = await db.question.find_many()
        
        if len(all_questions) < 10:
            raise HTTPException(
                status_code=400, 
                detail="Not enough questions in database. Need at least 10."
            )
        
        # Выбираем 10 случайных вопросов
        random_questions = random.sample(all_questions, 10)
        return random_questions
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Question])
async def get_all_questions(db=Depends(get_db)):
    """Получение всех вопросов"""
    questions = await db.question.find_many()
    return questions

@router.get("/{question_id}", response_model=Question)
async def get_question(question_id: int, db=Depends(get_db)):
    """Получение вопроса по ID"""
    question = await db.question.find_unique(
        where={"id": question_id}
    )
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    return question