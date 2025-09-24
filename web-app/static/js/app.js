// Глобальные переменные
let currentUser = null;
let currentTest = null;
let questions = [];
let currentQuestionIndex = 0;
let userAnswers = [];
let startTime = null;
let timerInterval = null;
let testStartTime = null;

// Telegram Web App
const tg = window.Telegram?.WebApp;

// Инициализация приложения
document.addEventListener('DOMContentLoaded', function() {
    initializeTelegramWebApp();
    initializeTheme();
    bindEventListeners();
    showScreen('welcomeScreen');
});

// Инициализация Telegram Web App
function initializeTelegramWebApp() {
    if (tg) {
        tg.ready();
        tg.expand();
        
        // Получаем данные пользователя из Telegram
        if (tg.initDataUnsafe?.user) {
            const user = tg.initDataUnsafe.user;
            createUser({
                telegramId: user.id.toString(),
                username: user.username,
                firstName: user.first_name,
                lastName: user.last_name
            });
        }
    }
}

// Инициализация темы
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeButton(savedTheme);
}

// Обновление кнопки темы
function updateThemeButton(theme) {
    const themeIcon = document.querySelector('.theme-icon');
    const themeText = document.querySelector('.theme-text');
    
    if (theme === 'dark') {
        themeIcon.textContent = '☀️';
        themeText.textContent = 'Светлая тема';
    } else {
        themeIcon.textContent = '🌙';
        themeText.textContent = 'Темная тема';
    }
}

// Привязка обработчиков событий
function bindEventListeners() {
    // Переключатель темы
    document.getElementById('themeToggle').addEventListener('click', toggleTheme);
    
    // Кнопки на главном экране
    document.getElementById('startTestBtn').addEventListener('click', startTest);
    document.getElementById('leaderboardBtn').addEventListener('click', showLeaderboard);
    
    // Кнопки в тесте
    document.getElementById('backBtn').addEventListener('click', previousQuestion);
    document.getElementById('nextBtn').addEventListener('click', nextQuestion);
    
    // Варианты ответов
    document.querySelectorAll('.option-btn').forEach(btn => {
        btn.addEventListener('click', selectAnswer);
    });
    
    // Кнопки результатов
    document.getElementById('retakeBtn').addEventListener('click', retakeTest);
    document.getElementById('homeBtn').addEventListener('click', () => showScreen('welcomeScreen'));
    document.getElementById('suggestionsBtn').addEventListener('click', openSuggestions);
    
    // Кнопки таблицы лидеров
    document.getElementById('backToHomeBtn').addEventListener('click', () => showScreen('welcomeScreen'));
    
    // Кнопки оплаты
    document.getElementById('payBtn').addEventListener('click', processPayment);
    document.getElementById('cancelPayBtn').addEventListener('click', () => showScreen('welcomeScreen'));
}

// Переключение темы
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeButton(newTheme);
}

// Показать экран
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
}

// Показать/скрыть загрузку
function showLoading(show = true) {
    const loading = document.getElementById('loading');
    if (show) {
        loading.classList.remove('hidden');
    } else {
        loading.classList.add('hidden');
    }
}

// API вызовы
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(`/api${endpoint}`, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Создание пользователя
async function createUser(userData) {
    try {
        currentUser = await apiCall('/users/', 'POST', userData);
        console.log('User created/retrieved:', currentUser);
    } catch (error) {
        console.error('Error creating user:', error);
    }
}

// Начало теста
async function startTest() {
    if (!currentUser) {
        alert('Ошибка: пользователь не определен');
        return;
    }
    
    try {
        showLoading();
        
        // Проверяем, может ли пользователь пройти тест
        const paymentCheck = await apiCall(`/telegram/payment/${currentUser.id}/check`);
        
        if (!paymentCheck.canRetake && paymentCheck.needPayment) {
            showLoading(false);
            showScreen('paymentScreen');
            return;
        }
        
        // Получаем вопросы
        questions = await apiCall('/questions/random');
        
        if (questions.length < 10) {
            throw new Error('Недостаточно вопросов в базе данных');
        }
        
        // Создаем новый тест
        currentTest = await apiCall('/tests/start', 'POST', { userId: currentUser.id });
        
        // Инициализируем тест
        currentQuestionIndex = 0;
        userAnswers = [];
        testStartTime = new Date();
        
        showLoading(false);
        showScreen('testScreen');
        displayQuestion();
        startTimer();
        
    } catch (error) {
        showLoading(false);
        alert('Ошибка при загрузке теста: ' + error.message);
    }
}

// Отображение вопроса
function displayQuestion() {
    const question = questions[currentQuestionIndex];
    
    document.getElementById('questionText').textContent = question.text;
    document.getElementById('option1').textContent = question.option1;
    document.getElementById('option2').textContent = question.option2;
    document.getElementById('option3').textContent = question.option3;
    document.getElementById('option4').textContent = question.option4;
    
    // Обновляем счетчик
    document.getElementById('questionCounter').textContent = `${currentQuestionIndex + 1}/10`;
    
    // Очищаем выбранные ответы
    document.querySelectorAll('.option-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    // Восстанавливаем предыдущий ответ, если есть
    const previousAnswer = userAnswers[currentQuestionIndex];
    if (previousAnswer) {
        const selectedBtn = document.querySelector(`[data-option="${previousAnswer}"]`);
        if (selectedBtn) {
            selectedBtn.classList.add('selected');
        }
    }
    
    // Управление кнопками
    document.getElementById('backBtn').disabled = currentQuestionIndex === 0;
    document.getElementById('nextBtn').disabled = !userAnswers[currentQuestionIndex];
    
    // Меняем текст кнопки "Далее" на последнем вопросе
    const nextBtn = document.getElementById('nextBtn');
    if (currentQuestionIndex === 9) {
        nextBtn.textContent = 'Завершить тест';
    } else {
        nextBtn.textContent = 'Далее';
    }
}

// Выбор ответа
function selectAnswer(event) {
    const selectedOption = parseInt(event.currentTarget.dataset.option);
    
    // Убираем выделение с других вариантов
    document.querySelectorAll('.option-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    // Выделяем выбранный вариант
    event.currentTarget.classList.add('selected');
    
    // Сохраняем ответ
    userAnswers[currentQuestionIndex] = selectedOption;
    
    // Активируем кнопку "Далее"
    document.getElementById('nextBtn').disabled = false;
}

// Предыдущий вопрос
function previousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
    }
}

// Следующий вопрос
async function nextQuestion() {
    // Сохраняем ответ на сервере
    const question = questions[currentQuestionIndex];
    const userAnswer = userAnswers[currentQuestionIndex];
    
    try {
        await apiCall(`/tests/${currentTest.id}/answer`, 'POST', {
            questionId: question.id,
            userAnswer: userAnswer
        });
    } catch (error) {
        console.error('Error saving answer:', error);
    }
    
    if (currentQuestionIndex < 9) {
        currentQuestionIndex++;
        displayQuestion();
    } else {
        // Завершаем тест
        await finishTest();
    }
}

// Завершение теста
async function finishTest() {
    try {
        showLoading();
        
        const endTime = new Date();
        const totalTime = Math.floor((endTime - testStartTime) / 1000);
        
        stopTimer();
        
        // Отправляем результаты на сервер
        const result = await apiCall(`/tests/${currentTest.id}/finish`, 'POST', totalTime);
        
        showLoading(false);
        displayResults(result);
        
    } catch (error) {
        showLoading(false);
        alert('Ошибка при завершении теста: ' + error.message);
    }
}

// Отображение результатов
function displayResults(result) {
    showScreen('resultsScreen');
    
    const resultTitle = document.getElementById('resultTitle');
    const correctAnswers = document.getElementById('correctAnswers');
    const totalTime = document.getElementById('totalTime');
    const wrongAnswersDiv = document.getElementById('wrongAnswers');
    
    // Заголовок
    if (result.isPassed) {
        resultTitle.textContent = '🎉 Поздравляем! Тест пройден!';
        resultTitle.className = 'result-title passed';
    } else {
        resultTitle.textContent = '😞 Тест не пройден';
        resultTitle.className = 'result-title failed';
    }
    
    // Статистика
    correctAnswers.textContent = `${result.score}/10`;
    totalTime.textContent = formatTime(result.totalTime);
    
    // Неправильные ответы
    wrongAnswersDiv.innerHTML = '';
    if (result.answers) {
        const wrongAnswers = result.answers.filter(answer => !answer.isCorrect);
        
        if (wrongAnswers.length > 0) {
            wrongAnswersDiv.innerHTML = '<h3>Неправильные ответы:</h3>';
            
            wrongAnswers.forEach(answer => {
                const question = questions.find(q => q.id === answer.questionId);
                if (question) {
                    const div = document.createElement('div');
                    div.className = 'wrong-answer';
                    
                    const optionText = question[`option${answer.userAnswer}`];
                    const correctText = question[`option${question.correctAnswer}`];
                    
                    div.innerHTML = `
                        <div class="wrong-answer-question">${question.text}</div>
                        <div class="wrong-answer-your">Ваш ответ: ${optionText}</div>
                        <div class="wrong-answer-correct">Правильный ответ: ${correctText}</div>
                    `;
                    
                    wrongAnswersDiv.appendChild(div);
                }
            });
        }
    }
}

// Таймер
function startTimer() {
    startTime = new Date();
    timerInterval = setInterval(updateTimer, 1000);
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

function updateTimer() {
    if (!startTime) return;
    
    const now = new Date();
    const elapsed = Math.floor((now - startTime) / 1000);
    document.getElementById('timer').textContent = formatTime(elapsed);
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

// Повторное прохождение теста
async function retakeTest() {
    if (!currentUser) return;
    
    try {
        const paymentCheck = await apiCall(`/telegram/payment/${currentUser.id}/check`);
        
        if (!paymentCheck.canRetake && paymentCheck.needPayment) {
            showScreen('paymentScreen');
        } else {
            startTest();
        }
    } catch (error) {
        alert('Ошибка при проверке возможности пересдачи: ' + error.message);
    }
}

// Таблица лидеров
async function showLeaderboard() {
    try {
        showLoading();
        
        const leaderboard = await apiCall('/tests/leaderboard');
        
        const tableDiv = document.getElementById('leaderboardTable');
        tableDiv.innerHTML = '';
        
        // Заголовок
        const header = document.createElement('div');
        header.className = 'leaderboard-header';
        header.innerHTML = `
            <div>#</div>
            <div>Пользователь</div>
            <div>Результат</div>
            <div class="time-col">Время</div>
            <div>Статус</div>
        `;
        tableDiv.appendChild(header);
        
        // Строки с результатами
        leaderboard.forEach((entry, index) => {
            const row = document.createElement('div');
            row.className = 'leaderboard-row';
            
            const status = entry.isPassed ? 'Пройден' : 'Не пройден';
            const statusClass = entry.isPassed ? 'passed' : 'failed';
            
            row.innerHTML = `
                <div class="leaderboard-position">${index + 1}</div>
                <div>${entry.username}</div>
                <div>${entry.score}/10</div>
                <div class="time-col">${formatTime(entry.totalTime)}</div>
                <div class="leaderboard-status ${statusClass}">${status}</div>
            `;
            
            tableDiv.appendChild(row);
        });
        
        showLoading(false);
        showScreen('leaderboardScreen');
        
    } catch (error) {
        showLoading(false);
        alert('Ошибка при загрузке таблицы лидеров: ' + error.message);
    }
}

// Оплата
function processPayment() {
    if (!tg) {
        alert('Оплата доступна только в Telegram');
        return;
    }
    
    // Создаем инвойс для оплаты
    const invoice = {
        title: 'Пересдача теста',
        description: 'Оплата за возможность пройти тест повторно',
        payload: 'retake_test',
        provider_token: '', // Для Telegram Stars не нужен
        start_parameter: 'retake',
        currency: 'XTR', // Telegram Stars
        prices: [{ label: 'Пересдача теста', amount: 200 }]
    };
    
    tg.invokeCustomMethod('web_app_trigger_haptic_feedback', { type: 'impact', impact_style: 'medium' });
    
    // Отправляем инвойс
    tg.sendData(JSON.stringify({ action: 'create_invoice', invoice }));
}

// Предложения и идеи
function openSuggestions() {
    if (tg) {
        // Открываем чат с админом
        const adminUsername = 'your_admin_username'; // Замените на реальный username админа
        tg.openTelegramLink(`https://t.me/${adminUsername}`);
    } else {
        alert('Функция доступна только в Telegram');
    }
}

// Обработка событий от Telegram
if (tg) {
    // Обработка закрытия приложения
    tg.onEvent('mainButtonClicked', function() {
        // Действия при нажатии главной кнопки
    });
    
    // Обработка изменений в viewport
    tg.onEvent('viewportChanged', function() {
        // Адаптация под изменения размера
    });
}