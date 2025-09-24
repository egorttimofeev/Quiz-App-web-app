from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List, Dict, Any, Optional
import os
import random
import json
import ipaddress
from datetime import datetime
from dotenv import load_dotenv

# Импортируем базу данных
try:
    from simple_db import db
except ImportError:
    print("❌ Ошибка импорта simple_db")
    db = None

# Загрузка переменных окружения из родительской папки
load_dotenv("../.env")

app = FastAPI(
    title="Quiz App API",
    description="API for Quiz Application with Telegram integration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение статических файлов (опционально)
try:
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
    
    # Проверяем существование папок
    static_dir = "../web-app/static"
    templates_dir = "../web-app/templates"
    
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    if os.path.exists(templates_dir):
        templates = Jinja2Templates(directory=templates_dir)
    else:
        templates = None
        
except ImportError:
    print("⚠️ StaticFiles или Jinja2Templates не доступны")
    templates = None

# === API ROUTES ===

# Пользователи
@app.post("/api/users/")
async def create_user(user_data: Dict[str, Any]):
    """Создание нового пользователя или получение существующего"""
    try:
        user = db.create_user(
            telegram_id=user_data["telegramId"],
            username=user_data.get("username"),
            first_name=user_data.get("firstName"),
            last_name=user_data.get("lastName")
        )
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/users/{telegram_id}")
async def get_user(telegram_id: str):
    """Получение пользователя по Telegram ID"""
    user = db.get_user_by_telegram_id(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Вопросы
@app.get("/api/questions/random")
async def get_random_questions():
    """Получение 10 случайных вопросов для теста"""
    try:
        if db.get_questions_count() < 10:
            raise HTTPException(
                status_code=400, 
                detail="Not enough questions in database. Need at least 10."
            )
        
        questions = db.get_random_questions(10)
        return questions
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/questions/")
async def create_question(question_data: Dict[str, Any]):
    """Создание нового вопроса"""
    try:
        question = db.create_question(
            text=question_data["text"],
            option1=question_data["option1"],
            option2=question_data["option2"],
            option3=question_data["option3"],
            option4=question_data["option4"],
            correct_answer=question_data["correctAnswer"]
        )
        return question
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Тесты
@app.post("/api/tests/start")
async def start_test(test_data: Dict[str, Any]):
    """Начало нового теста"""
    try:
        test = db.create_test(user_id=test_data["userId"])
        return test
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/tests/{test_id}/answer")
async def submit_answer(test_id: int, answer_data: Dict[str, Any]):
    """Отправка ответа на вопрос"""
    try:
        question = db.get_question_by_id(answer_data["questionId"])
        
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        is_correct = question["correctAnswer"] == answer_data["userAnswer"]
        
        db.create_test_answer(
            test_id=test_id,
            question_id=answer_data["questionId"],
            user_answer=answer_data["userAnswer"],
            is_correct=is_correct
        )
        
        return {"success": True, "isCorrect": is_correct}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/tests/{test_id}/finish")
async def finish_test(test_id: int, total_time: int):
    """Завершение теста и подсчет результатов"""
    try:
        # Получаем ответы теста
        answers = db.get_test_answers(test_id)
        
        # Подсчитываем правильные ответы
        correct_answers = sum(1 for answer in answers if answer["isCorrect"])
        is_passed = correct_answers >= 7  # 70% для прохождения
        
        # Завершаем тест
        db.finish_test(test_id, total_time, correct_answers, is_passed)
        
        return {
            "success": True,
            "score": correct_answers,
            "totalQuestions": 10,
            "totalTime": total_time,
            "isPassed": is_passed,
            "answers": answers
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/tests/leaderboard")
async def get_leaderboard():
    """Получение таблицы лидеров"""
    try:
        leaderboard = db.get_leaderboard(100)
        return leaderboard
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Telegram
@app.get("/api/telegram/payment/{user_id}/check")
async def check_user_payment(user_id: int):
    """Проверка, может ли пользователь пересдать тест"""
    try:
        test_count = db.get_user_test_count(user_id)
        
        if test_count == 0:
            return {"canRetake": True, "needPayment": False}
        
        payments_count = db.get_user_payments_count(user_id)
        available_retakes = payments_count
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

# === WEB ROUTES ===

# === WEB ROUTES ===

@app.get("/")
async def root():
    """Главная страница"""
    return {
        "message": "Quiz App API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "questions": "/api/questions/random",
            "users": "/api/users/",
            "tests": "/api/tests/start",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья API"""
    try:
        # Проверяем базу данных
        if db:
            count = db.get_questions_count()
            return {
                "status": "healthy",
                "database": "connected", 
                "questions_count": count
            }
        else:
            return {
                "status": "degraded",
                "database": "disconnected"
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.get("/app", response_class=HTMLResponse)
async def web_app():
    """Telegram Web App - Квиз приложение"""
    html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz Master</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--tg-theme-bg-color, #f5f5f5);
            color: var(--tg-theme-text-color, #333);
            padding: 0;
            margin: 0;
            user-select: none;
            -webkit-user-select: none;
            overflow-x: hidden;
        }
        
        .container {
            max-width: 100%;
            padding: 20px 16px;
            min-height: 100vh;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px 0;
        }
        
        .logo {
            font-size: 48px;
            margin-bottom: 10px;
        }
        
        .title {
            font-size: 28px;
            font-weight: 700;
            color: var(--tg-theme-link-color, #0088cc);
            margin-bottom: 8px;
        }
        
        .subtitle {
            font-size: 16px;
            color: var(--tg-theme-hint-color, #999);
        }
        
        .user-info {
            background: var(--tg-theme-secondary-bg-color, #fff);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 24px;
            text-align: center;
            border: 1px solid var(--tg-theme-section-separator-color, #e5e5e5);
        }
        
        .user-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--tg-theme-link-color, #0088cc);
            color: white;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 12px;
        }
        
        .btn {
            width: 100%;
            background: var(--tg-theme-button-color, #0088cc);
            color: var(--tg-theme-button-text-color, white);
            border: none;
            padding: 16px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            margin: 8px 0;
            transition: opacity 0.2s;
            position: relative;
            overflow: hidden;
        }
        
        .btn:active {
            opacity: 0.8;
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .btn-success {
            background: #28a745;
        }
        
        .btn-warning {
            background: #ffc107;
            color: #000;
        }
        
        .quiz-screen {
            display: none;
        }
        
        .quiz-screen.active {
            display: block;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: var(--tg-theme-section-separator-color, #e5e5e5);
            border-radius: 4px;
            margin-bottom: 24px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: var(--tg-theme-link-color, #0088cc);
            border-radius: 4px;
            transition: width 0.3s ease;
            width: 0%;
        }
        
        .question-card {
            background: var(--tg-theme-secondary-bg-color, #fff);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            border: 1px solid var(--tg-theme-section-separator-color, #e5e5e5);
        }
        
        .question-number {
            font-size: 14px;
            color: var(--tg-theme-hint-color, #999);
            margin-bottom: 8px;
        }
        
        .question-text {
            font-size: 18px;
            font-weight: 600;
            line-height: 1.4;
            margin-bottom: 20px;
        }
        
        .option {
            background: var(--tg-theme-bg-color, #f5f5f5);
            border: 2px solid var(--tg-theme-section-separator-color, #e5e5e5);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
        }
        
        .option:hover {
            border-color: var(--tg-theme-link-color, #0088cc);
        }
        
        .option.selected {
            border-color: var(--tg-theme-link-color, #0088cc);
            background: var(--tg-theme-link-color, #0088cc);
            color: white;
        }
        
        .option.correct {
            border-color: #28a745;
            background: #28a745;
            color: white;
        }
        
        .option.incorrect {
            border-color: #dc3545;
            background: #dc3545;
            color: white;
        }
        
        .timer {
            background: var(--tg-theme-secondary-bg-color, #fff);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            margin-bottom: 24px;
            border: 1px solid var(--tg-theme-section-separator-color, #e5e5e5);
        }
        
        .timer-text {
            font-size: 24px;
            font-weight: 700;
            color: var(--tg-theme-link-color, #0088cc);
        }
        
        .timer.warning .timer-text {
            color: #ffc107;
        }
        
        .timer.danger .timer-text {
            color: #dc3545;
        }
        
        .result-screen {
            text-align: center;
            padding: 40px 20px;
        }
        
        .result-icon {
            font-size: 80px;
            margin-bottom: 20px;
        }
        
        .result-title {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 12px;
        }
        
        .result-score {
            font-size: 48px;
            font-weight: 800;
            color: var(--tg-theme-link-color, #0088cc);
            margin: 20px 0;
        }
        
        .stats {
            background: var(--tg-theme-secondary-bg-color, #fff);
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
            border: 1px solid var(--tg-theme-section-separator-color, #e5e5e5);
        }
        
        .stat-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid var(--tg-theme-section-separator-color, #e5e5e5);
        }
        
        .stat-row:last-child {
            border-bottom: none;
        }
        
        .payment-info {
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 12px;
            padding: 16px;
            margin: 20px 0;
            text-align: center;
        }
        
        .hidden {
            display: none !important;
        }
        
        @media (max-width: 480px) {
            .container {
                padding: 16px 12px;
            }
            
            .title {
                font-size: 24px;
            }
            
            .question-text {
                font-size: 16px;
            }
        }
    </style>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body>
    <div class="container">
        <!-- Главный экран -->
        <div id="main-screen" class="screen">
            <div class="header">
                <div class="logo">🎯</div>
                <div class="title">Quiz Master</div>
                <div class="subtitle">Проверь свои знания!</div>
            </div>
            
            <div class="user-info" id="user-info">
                <div class="user-avatar" id="user-avatar">?</div>
                <div id="user-name">Загрузка...</div>
                <div id="user-stats" style="font-size: 14px; color: #999; margin-top: 8px;">
                    Пройдено тестов: <span id="tests-count">0</span>
                </div>
            </div>
            
            <button class="btn" onclick="startNewTest()" id="start-btn">
                🚀 Начать новый тест
            </button>
            
            <button class="btn btn-success" onclick="showLeaderboard()">
                🏆 Таблица лидеров
            </button>
            
            <button class="btn" onclick="showSettings()" style="background: #6c757d;">
                ⚙️ Настройки
            </button>
        </div>
        
        <!-- Экран квиза -->
        <div id="quiz-screen" class="screen quiz-screen">
            <div class="progress-bar">
                <div class="progress-fill" id="progress"></div>
            </div>
            
            <div class="timer" id="timer">
                <div class="timer-text" id="timer-text">05:00</div>
                <div style="font-size: 12px; margin-top: 4px;">Осталось времени</div>
            </div>
            
            <div class="question-card">
                <div class="question-number" id="question-number">Вопрос 1 из 10</div>
                <div class="question-text" id="question-text">Загрузка вопроса...</div>
            </div>
            
            <div id="options-container">
                <!-- Варианты ответов будут добавлены динамически -->
            </div>
            
            <button class="btn" id="next-btn" onclick="nextQuestion()" disabled>
                Следующий вопрос
            </button>
        </div>
        
        <!-- Экран результатов -->
        <div id="result-screen" class="screen hidden">
            <div class="result-screen">
                <div class="result-icon" id="result-icon">🎉</div>
                <div class="result-title" id="result-title">Отлично!</div>
                <div class="result-score" id="result-score">0/10</div>
                
                <div class="stats">
                    <div class="stat-row">
                        <span>Правильных ответов:</span>
                        <span id="correct-count">0</span>
                    </div>
                    <div class="stat-row">
                        <span>Неправильных ответов:</span>
                        <span id="incorrect-count">0</span>
                    </div>
                    <div class="stat-row">
                        <span>Время прохождения:</span>
                        <span id="completion-time">0:00</span>
                    </div>
                    <div class="stat-row">
                        <span>Процент правильных:</span>
                        <span id="success-rate">0%</span>
                    </div>
                </div>
                
                <div id="payment-section" class="payment-info hidden">
                    <div style="font-weight: 600; margin-bottom: 8px;">💫 Хотите попробовать еще раз?</div>
                    <div style="font-size: 14px; margin-bottom: 12px;">
                        Повторное прохождение стоит 200 Telegram Stars
                    </div>
                    <button class="btn btn-warning" onclick="requestPayment()">
                        ⭐ Оплатить и попробовать снова
                    </button>
                </div>
                
                <button class="btn" onclick="showMainScreen()">
                    🏠 На главную
                </button>
                
                <button class="btn btn-success" onclick="shareResult()">
                    📤 Поделиться результатом
                </button>
            </div>
        </div>
    </div>
    
    <script>
        // Глобальные переменные
        let currentUser = null;
        let currentTest = null;
        let currentQuestionIndex = 0;
        let questions = [];
        let answers = [];
        let timer = null;
        let timeLeft = 300; // 5 минут
        let testStartTime = null;
        
        // Telegram Web App API
        const tg = window.Telegram?.WebApp;
        
        // Инициализация приложения
        window.onload = async function() {
            if (tg) {
                tg.ready();
                tg.expand();
                tg.MainButton.hide();
                
                // Применяем тему Telegram
                document.body.style.setProperty('--tg-theme-bg-color', tg.themeParams.bg_color || '#ffffff');
                document.body.style.setProperty('--tg-theme-text-color', tg.themeParams.text_color || '#000000');
                document.body.style.setProperty('--tg-theme-hint-color', tg.themeParams.hint_color || '#999999');
                document.body.style.setProperty('--tg-theme-link-color', tg.themeParams.link_color || '#0088cc');
                document.body.style.setProperty('--tg-theme-button-color', tg.themeParams.button_color || '#0088cc');
                document.body.style.setProperty('--tg-theme-button-text-color', tg.themeParams.button_text_color || '#ffffff');
            }
            
            await initUser();
            await loadUserStats();
        };
        
        // Инициализация пользователя
        async function initUser() {
            try {
                if (tg && tg.initDataUnsafe && tg.initDataUnsafe.user) {
                    const user = tg.initDataUnsafe.user;
                    currentUser = user;
                    
                    document.getElementById('user-name').textContent = user.first_name + (user.last_name ? ' ' + user.last_name : '');
                    document.getElementById('user-avatar').textContent = user.first_name[0].toUpperCase();
                    
                    // Создаем или получаем пользователя в системе
                    const response = await fetch('/api/users/', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            telegramId: user.id,
                            username: user.username || null,
                            firstName: user.first_name,
                            lastName: user.last_name || null
                        })
                    });
                } else {
                    // Режим разработки - создаем тестового пользователя
                    document.getElementById('user-name').textContent = 'Тестовый пользователь';
                    document.getElementById('user-avatar').textContent = 'T';
                    currentUser = { id: 'test', first_name: 'Test' };
                }
            } catch (error) {
                console.error('Ошибка инициализации пользователя:', error);
                document.getElementById('user-name').textContent = 'Гость';
                document.getElementById('user-avatar').textContent = 'Г';
            }
        }
        
        // Загрузка статистики пользователя
        async function loadUserStats() {
            try {
                // Здесь будет запрос к API для получения статистики
                document.getElementById('tests-count').textContent = '0';
            } catch (error) {
                console.error('Ошибка загрузки статистики:', error);
            }
        }
        
        // Начать новый тест
        async function startNewTest() {
            try {
                document.getElementById('start-btn').disabled = true;
                document.getElementById('start-btn').textContent = 'Загрузка...';
                
                // Загружаем вопросы
                const response = await fetch('/api/questions/random');
                questions = await response.json();
                
                if (questions.length === 0) {
                    alert('Не найдено вопросов для теста!');
                    return;
                }
                
                // Инициализируем тест
                currentQuestionIndex = 0;
                answers = [];
                timeLeft = 300;
                testStartTime = Date.now();
                
                showQuizScreen();
                startTimer();
                showCurrentQuestion();
                
            } catch (error) {
                console.error('Ошибка запуска теста:', error);
                alert('Ошибка загрузки теста!');
            } finally {
                document.getElementById('start-btn').disabled = false;
                document.getElementById('start-btn').textContent = '🚀 Начать новый тест';
            }
        }
        
        // Показать экран квиза
        function showQuizScreen() {
            document.getElementById('main-screen').classList.add('hidden');
            document.getElementById('quiz-screen').classList.remove('hidden');
            document.getElementById('quiz-screen').classList.add('active');
        }
        
        // Показать главный экран
        function showMainScreen() {
            document.getElementById('quiz-screen').classList.add('hidden');
            document.getElementById('result-screen').classList.add('hidden');
            document.getElementById('main-screen').classList.remove('hidden');
            
            if (timer) {
                clearInterval(timer);
                timer = null;
            }
        }
        
        // Показать текущий вопрос
        function showCurrentQuestion() {
            const question = questions[currentQuestionIndex];
            const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
            
            document.getElementById('progress').style.width = progress + '%';
            document.getElementById('question-number').textContent = `Вопрос ${currentQuestionIndex + 1} из ${questions.length}`;
            document.getElementById('question-text').textContent = question.text;
            
            const optionsContainer = document.getElementById('options-container');
            optionsContainer.innerHTML = '';
            
            const options = [
                { text: question.option1, value: 1 },
                { text: question.option2, value: 2 },
                { text: question.option3, value: 3 },
                { text: question.option4, value: 4 }
            ];
            
            options.forEach((option, index) => {
                const optionDiv = document.createElement('div');
                optionDiv.className = 'option';
                optionDiv.innerHTML = `<strong>${String.fromCharCode(65 + index)})</strong> ${option.text}`;
                optionDiv.onclick = () => selectOption(option.value, optionDiv);
                optionsContainer.appendChild(optionDiv);
            });
            
            document.getElementById('next-btn').disabled = true;
        }
        
        // Выбор варианта ответа
        function selectOption(value, element) {
            // Убираем выделение с других опций
            document.querySelectorAll('.option').forEach(opt => opt.classList.remove('selected'));
            
            // Выделяем выбранную опцию
            element.classList.add('selected');
            
            // Сохраняем ответ
            answers[currentQuestionIndex] = value;
            
            // Активируем кнопку "Следующий вопрос"
            document.getElementById('next-btn').disabled = false;
        }
        
        // Следующий вопрос
        function nextQuestion() {
            currentQuestionIndex++;
            
            if (currentQuestionIndex < questions.length) {
                showCurrentQuestion();
            } else {
                finishTest();
            }
        }
        
        // Завершить тест
        function finishTest() {
            if (timer) {
                clearInterval(timer);
                timer = null;
            }
            
            const completionTime = Math.floor((Date.now() - testStartTime) / 1000);
            let correctCount = 0;
            
            // Подсчитываем правильные ответы
            for (let i = 0; i < questions.length; i++) {
                if (answers[i] === questions[i].correctAnswer) {
                    correctCount++;
                }
            }
            
            showResults(correctCount, questions.length, completionTime);
        }
        
        // Показать результаты
        function showResults(correct, total, timeSeconds) {
            const percentage = Math.round((correct / total) * 100);
            const minutes = Math.floor(timeSeconds / 60);
            const seconds = timeSeconds % 60;
            
            // Определяем иконку и заголовок по результату
            let icon, title;
            if (percentage >= 80) {
                icon = '🎉';
                title = 'Отлично!';
            } else if (percentage >= 60) {
                icon = '👏';
                title = 'Хорошо!';
            } else if (percentage >= 40) {
                icon = '👍';
                title = 'Неплохо!';
            } else {
                icon = '📚';
                title = 'Есть к чему стремиться!';
            }
            
            document.getElementById('result-icon').textContent = icon;
            document.getElementById('result-title').textContent = title;
            document.getElementById('result-score').textContent = `${correct}/${total}`;
            document.getElementById('correct-count').textContent = correct;
            document.getElementById('incorrect-count').textContent = total - correct;
            document.getElementById('completion-time').textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            document.getElementById('success-rate').textContent = `${percentage}%`;
            
            // Показываем секцию оплаты, если результат меньше 80%
            if (percentage < 80) {
                document.getElementById('payment-section').classList.remove('hidden');
            } else {
                document.getElementById('payment-section').classList.add('hidden');
            }
            
            document.getElementById('quiz-screen').classList.add('hidden');
            document.getElementById('result-screen').classList.remove('hidden');
        }
        
        // Таймер
        function startTimer() {
            timer = setInterval(() => {
                timeLeft--;
                
                const minutes = Math.floor(timeLeft / 60);
                const seconds = timeLeft % 60;
                
                document.getElementById('timer-text').textContent = 
                    `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                
                const timerElement = document.getElementById('timer');
                if (timeLeft <= 60) {
                    timerElement.className = 'timer danger';
                } else if (timeLeft <= 120) {
                    timerElement.className = 'timer warning';
                }
                
                if (timeLeft <= 0) {
                    finishTest();
                }
            }, 1000);
        }
        
        // Запрос оплаты через Telegram Stars
        function requestPayment() {
            if (tg && tg.showPopup) {
                tg.showPopup({
                    title: '💫 Оплата',
                    message: 'Повторное прохождение теста стоит 200 Telegram Stars. Продолжить?',
                    buttons: [
                        {type: 'ok', text: 'Оплатить'},
                        {type: 'cancel', text: 'Отмена'}
                    ]
                }, (buttonId) => {
                    if (buttonId === 'ok') {
                        // Здесь будет интеграция с Telegram Stars API
                        alert('Функция оплаты будет доступна после настройки Telegram Stars API');
                    }
                });
            } else {
                alert('Оплата доступна только в Telegram Web App');
            }
        }
        
        // Поделиться результатом
        function shareResult() {
            const correct = document.getElementById('correct-count').textContent;
            const total = questions.length;
            const percentage = Math.round((correct / total) * 100);
            
            const shareText = `🎯 Я прошел квиз в Quiz Master!\\n✅ Правильных ответов: ${correct}/${total} (${percentage}%)\\n\\n🚀 Попробуй и ты!`;
            
            if (tg && tg.shareToStory) {
                tg.shareToStory(shareText);
            } else if (navigator.share) {
                navigator.share({
                    title: 'Quiz Master - Результат',
                    text: shareText
                });
            } else {
                navigator.clipboard.writeText(shareText);
                alert('Результат скопирован в буфер обмена!');
            }
        }
        
        // Заглушки для других функций
        function showLeaderboard() {
            alert('🏆 Таблица лидеров в разработке!');
        }
        
        function showSettings() {
            alert('⚙️ Настройки в разработке!');
        }
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

# Telegram Bot Webhook
@app.post("/webhook/{bot_token}")
async def telegram_webhook(bot_token: str, request: Request):
    """Webhook для получения обновлений от Telegram бота"""
    try:
        # Проверяем токен бота
        expected_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if expected_token and bot_token != expected_token:
            raise HTTPException(status_code=403, detail="Invalid bot token")
        
        # Получаем данные от Telegram
        update_data = await request.json()
        
        # Обрабатываем обновление
        await process_telegram_update(update_data)
        
        return {"ok": True}
    
    except Exception as e:
        print(f"❌ Ошибка webhook: {e}")
        return {"ok": False, "error": str(e)}

async def process_telegram_update(update: Dict[str, Any]):
    """Обработка обновлений от Telegram"""
    try:
        if "message" in update:
            message = update["message"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "")
            
            # Обработка команд
            if text == "/start":
                await send_welcome_message(chat_id)
            elif text == "/help":
                await send_help_message(chat_id)
            elif text == "/stats":
                await send_user_stats(chat_id)
            elif text == "/leaderboard":
                await send_leaderboard(chat_id)
                
        elif "pre_checkout_query" in update:
            # Обработка предварительного запроса оплаты
            await handle_pre_checkout(update["pre_checkout_query"])
            
        elif "successful_payment" in update:
            # Обработка успешной оплаты
            await handle_successful_payment(update["message"])
            
    except Exception as e:
        print(f"❌ Ошибка обработки обновления: {e}")

async def send_welcome_message(chat_id: int):
    """Отправка приветственного сообщения"""
    message = """🎯 **Добро пожаловать в Quiz Master!**

✨ **Что умеет бот:**
• 📝 Интерактивные квизы из 10 вопросов
• ⏱️ Таймер на 5 минут
• 📊 Система оценок и статистика
• 🔄 Повторные попытки за Telegram Stars
• 🏆 Таблица лидеров

🚀 **Нажмите кнопку "Квиз" в меню чтобы начать!**

💡 Используйте команды:
/help - помощь
/stats - ваша статистика
/leaderboard - топ игроков"""
    
    await send_telegram_message(chat_id, message)

async def send_help_message(chat_id: int):
    """Отправка сообщения помощи"""
    message = """ℹ️ **Помощь по Quiz Master**

🎮 **Как играть:**
1. Нажмите кнопку "🎯 Начать квиз" в меню
2. Ответьте на 10 вопросов за 5 минут
3. Получите результат и сравните с другими!

💫 **Повторные попытки:**
• Первая попытка - бесплатно
• Дополнительные попытки - 200 ⭐ Telegram Stars

📊 **Команды:**
/start - главное меню
/stats - ваша статистика  
/leaderboard - таблица лидеров
/help - это сообщение

❓ **Проблемы?** Свяжитесь с поддержкой."""
    
    await send_telegram_message(chat_id, message)

async def send_user_stats(chat_id: int):
    """Отправка статистики пользователя"""
    try:
        # Здесь будет запрос к базе данных для получения статистики
        stats_message = """📊 **Ваша статистика:**

🎯 Тестов пройдено: 0
✅ Правильных ответов: 0
📈 Средний результат: 0%
🏆 Лучший результат: 0%
⏱️ Среднее время: 0:00

🚀 Начните первый тест чтобы увидеть статистику!"""
        
        await send_telegram_message(chat_id, stats_message)
        
    except Exception as e:
        await send_telegram_message(chat_id, "❌ Ошибка получения статистики")

async def send_leaderboard(chat_id: int):
    """Отправка таблицы лидеров"""
    try:
        # Здесь будет запрос к базе данных для получения топа
        leaderboard_message = """🏆 **Таблица лидеров:**

1. 👤 Игрок 1 - 100%
2. 👤 Игрок 2 - 95%
3. 👤 Игрок 3 - 90%

📊 Всего игроков: 0
🎯 Ваше место: не в топе

🚀 Пройдите тест чтобы попасть в рейтинг!"""
        
        await send_telegram_message(chat_id, leaderboard_message)
        
    except Exception as e:
        await send_telegram_message(chat_id, "❌ Ошибка получения рейтинга")

async def send_telegram_message(chat_id: int, text: str, parse_mode: str = "Markdown"):
    """Отправка сообщения через Telegram Bot API"""
    try:
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            print("❌ TELEGRAM_BOT_TOKEN не установлен")
            return
            
        # Здесь будет HTTP запрос к Telegram Bot API
        # Для простоты пока только логируем
        print(f"📤 Отправка сообщения в чат {chat_id}: {text[:50]}...")
        
    except Exception as e:
        print(f"❌ Ошибка отправки сообщения: {e}")

async def handle_pre_checkout(pre_checkout_query: Dict[str, Any]):
    """Обработка предварительного запроса оплаты"""
    try:
        query_id = pre_checkout_query["id"]
        
        # Здесь можно добавить дополнительные проверки
        # Например, проверить доступность повторной попытки
        
        # Подтверждаем оплату
        print(f"✅ Подтверждение оплаты для запроса {query_id}")
        
    except Exception as e:
        print(f"❌ Ошибка обработки предоплаты: {e}")

async def handle_successful_payment(message: Dict[str, Any]):
    """Обработка успешной оплаты"""
    try:
        payment = message["successful_payment"]
        chat_id = message["chat"]["id"]
        
        # Записываем оплату в базу данных
        # Разрешаем повторную попытку
        
        success_message = """✅ **Оплата прошла успешно!**

🎯 Вы можете пройти тест еще раз!
💫 Списано: 200 ⭐ Telegram Stars

🚀 Нажмите кнопку "Квиз" чтобы начать!"""
        
        await send_telegram_message(chat_id, success_message)
        
    except Exception as e:
        print(f"❌ Ошибка обработки платежа: {e}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Запуск Quiz API сервера...")
    print("📝 Документация: http://localhost:8000/docs")
    print("🌐 Веб-приложение: http://localhost:8000/app")
    print()
    print("⚠️  Для Telegram Web App нужен HTTPS!")
    print("� Используйте ngrok для создания HTTPS туннеля:")
    print("   1. Установите ngrok: https://ngrok.com/download")
    print("   2. В другом терминале: ngrok http 8000")
    print("   3. Скопируйте https://xxx.ngrok.io URL")
    print("   4. В @BotFather используйте: https://xxx.ngrok.io/app")
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)

