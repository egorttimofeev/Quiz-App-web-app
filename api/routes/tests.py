from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime
from models.schemas import Test, TestCreate, TestAnswer, TestAnswerCreate, TestResult, TestResultCreate
from services.database import get_db

router = APIRouter()

@router.post("/start", response_model=Test)
async def start_test(test_data: TestCreate, db=Depends(get_db)):
    """Начало нового теста"""
    try:
        new_test = await db.test.create(
            data={
                "userId": test_data.userId,
            }
        )
        return new_test
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{test_id}/answer")
async def submit_answer(test_id: int, answer: TestAnswerCreate, db=Depends(get_db)):
    """Отправка ответа на вопрос"""
    try:
        # Получаем правильный ответ из базы
        question = await db.question.find_unique(
            where={"id": answer.questionId}
        )
        
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        is_correct = question.correctAnswer == answer.userAnswer
        
        # Сохраняем ответ
        new_answer = await db.testanswer.create(
            data={
                "testId": test_id,
                "questionId": answer.questionId,
                "userAnswer": answer.userAnswer,
                "isCorrect": is_correct,
            }
        )
        
        return {"success": True, "isCorrect": is_correct}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{test_id}/finish")
async def finish_test(test_id: int, total_time: int, db=Depends(get_db)):
    """Завершение теста и подсчет результатов"""
    try:
        # Получаем тест
        test = await db.test.find_unique(
            where={"id": test_id},
            include={"answers": True}
        )
        
        if not test:
            raise HTTPException(status_code=404, detail="Test not found")
        
        # Подсчитываем правильные ответы
        correct_answers = sum(1 for answer in test.answers if answer.isCorrect)
        is_passed = correct_answers >= 7  # 70% для прохождения
        
        # Обновляем тест
        updated_test = await db.test.update(
            where={"id": test_id},
            data={
                "finishedAt": datetime.now(),
                "totalTime": total_time,
                "score": correct_answers,
                "isPassed": is_passed,
            }
        )
        
        # Создаем результат теста
        test_result = await db.testresult.create(
            data={
                "testId": test_id,
                "userId": test.userId,
                "score": correct_answers,
                "totalTime": total_time,
                "isPassed": is_passed,
            }
        )
        
        return {
            "success": True,
            "score": correct_answers,
            "totalQuestions": 10,
            "totalTime": total_time,
            "isPassed": is_passed,
            "answers": test.answers
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{test_id}/result")
async def get_test_result(test_id: int, db=Depends(get_db)):
    """Получение результата теста"""
    try:
        result = await db.testresult.find_unique(
            where={"testId": test_id},
            include={
                "test": {
                    "include": {"answers": {"include": {"question": True}}}
                }
            }
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="Test result not found")
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/leaderboard", response_model=List[dict])
async def get_leaderboard(db=Depends(get_db)):
    """Получение таблицы лидеров"""
    try:
        results = await db.testresult.find_many(
            include={"user": True},
            order_by=[
                {"isPassed": "desc"},  # Сначала прошедшие тест
                {"score": "desc"},     # Потом по количеству правильных ответов
                {"totalTime": "asc"}   # Затем по времени (меньше = лучше)
            },
            take=100  # Топ 100
        )
        
        leaderboard = []
        for result in results:
            leaderboard.append({
                "username": result.user.username or result.user.firstName or "Anonymous",
                "score": result.score,
                "totalTime": result.totalTime,
                "isPassed": result.isPassed,
                "createdAt": result.createdAt
            })
        
        return leaderboard
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))