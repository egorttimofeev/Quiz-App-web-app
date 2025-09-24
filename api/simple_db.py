import sqlite3
import os
from typing import List, Dict, Any
import json
from datetime import datetime

class SimpleDB:
    """Простая база данных SQLite для замены Prisma"""
    
    def __init__(self, db_path: str = "quiz_app.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Создаем таблицы
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegramId TEXT UNIQUE NOT NULL,
                username TEXT,
                firstName TEXT,
                lastName TEXT,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                option1 TEXT NOT NULL,
                option2 TEXT NOT NULL,
                option3 TEXT NOT NULL,
                option4 TEXT NOT NULL,
                correctAnswer INTEGER NOT NULL,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId INTEGER NOT NULL,
                startedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                finishedAt TIMESTAMP NULL,
                isPassed BOOLEAN NULL,
                totalTime INTEGER NULL,
                score INTEGER NULL,
                FOREIGN KEY (userId) REFERENCES users(id)
            );
            
            CREATE TABLE IF NOT EXISTS test_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                testId INTEGER NOT NULL,
                questionId INTEGER NOT NULL,
                userAnswer INTEGER NOT NULL,
                isCorrect BOOLEAN NOT NULL,
                FOREIGN KEY (testId) REFERENCES tests(id),
                FOREIGN KEY (questionId) REFERENCES questions(id),
                UNIQUE(testId, questionId)
            );
            
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                testId INTEGER UNIQUE NOT NULL,
                userId INTEGER NOT NULL,
                score INTEGER NOT NULL,
                totalTime INTEGER NOT NULL,
                isPassed BOOLEAN NOT NULL,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (testId) REFERENCES tests(id),
                FOREIGN KEY (userId) REFERENCES users(id)
            );
            
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId INTEGER NOT NULL,
                telegramPaymentId TEXT UNIQUE NOT NULL,
                amount INTEGER NOT NULL,
                status TEXT NOT NULL,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (userId) REFERENCES users(id)
            );
        """)
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Получить подключение к БД"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Возвращать строки как dict
        return conn
    
    # Пользователи
    def create_user(self, telegram_id: str, username: str = None, 
                   first_name: str = None, last_name: str = None) -> Dict:
        """Создать пользователя"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO users (telegramId, username, firstName, lastName)
                VALUES (?, ?, ?, ?)
            """, (telegram_id, username, first_name, last_name))
            
            user_id = cursor.lastrowid
            conn.commit()
            
            return self.get_user_by_telegram_id(telegram_id)
        except sqlite3.IntegrityError:
            # Пользователь уже существует
            return self.get_user_by_telegram_id(telegram_id)
        finally:
            conn.close()
    
    def get_user_by_telegram_id(self, telegram_id: str) -> Dict:
        """Получить пользователя по Telegram ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE telegramId = ?", (telegram_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_user_by_id(self, user_id: int) -> Dict:
        """Получить пользователя по ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    # Вопросы
    def create_question(self, text: str, option1: str, option2: str, 
                       option3: str, option4: str, correct_answer: int) -> Dict:
        """Создать вопрос"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO questions (text, option1, option2, option3, option4, correctAnswer)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (text, option1, option2, option3, option4, correct_answer))
        
        question_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return self.get_question_by_id(question_id)
    
    def get_question_by_id(self, question_id: int) -> Dict:
        """Получить вопрос по ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_random_questions(self, count: int = 10) -> List[Dict]:
        """Получить случайные вопросы"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT ?", (count,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_questions_count(self) -> int:
        """Получить количество вопросов"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM questions")
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    # Тесты
    def create_test(self, user_id: int) -> Dict:
        """Создать тест"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO tests (userId) VALUES (?)", (user_id,))
        test_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {"id": test_id, "userId": user_id}
    
    def create_test_answer(self, test_id: int, question_id: int, 
                          user_answer: int, is_correct: bool):
        """Сохранить ответ на вопрос"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO test_answers (testId, questionId, userAnswer, isCorrect)
            VALUES (?, ?, ?, ?)
        """, (test_id, question_id, user_answer, is_correct))
        
        conn.commit()
        conn.close()
    
    def finish_test(self, test_id: int, total_time: int, score: int, is_passed: bool):
        """Завершить тест"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Обновляем тест
        cursor.execute("""
            UPDATE tests 
            SET finishedAt = CURRENT_TIMESTAMP, totalTime = ?, score = ?, isPassed = ?
            WHERE id = ?
        """, (total_time, score, is_passed, test_id))
        
        # Получаем userId
        cursor.execute("SELECT userId FROM tests WHERE id = ?", (test_id,))
        user_id = cursor.fetchone()[0]
        
        # Создаем результат
        cursor.execute("""
            INSERT INTO test_results (testId, userId, score, totalTime, isPassed)
            VALUES (?, ?, ?, ?, ?)
        """, (test_id, user_id, score, total_time, is_passed))
        
        conn.commit()
        conn.close()
    
    def get_test_answers(self, test_id: int) -> List[Dict]:
        """Получить ответы теста"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ta.*, q.text as questionText, q.correctAnswer,
                   q.option1, q.option2, q.option3, q.option4
            FROM test_answers ta
            JOIN questions q ON ta.questionId = q.id
            WHERE ta.testId = ?
        """, (test_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_leaderboard(self, limit: int = 100) -> List[Dict]:
        """Получить таблицу лидеров"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT u.username, u.firstName, tr.score, tr.totalTime, 
                   tr.isPassed, tr.createdAt
            FROM test_results tr
            JOIN users u ON tr.userId = u.id
            ORDER BY tr.isPassed DESC, tr.score DESC, tr.totalTime ASC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            row_dict = dict(row)
            username = row_dict['username'] or row_dict['firstName'] or 'Anonymous'
            results.append({
                'username': username,
                'score': row_dict['score'],
                'totalTime': row_dict['totalTime'],
                'isPassed': row_dict['isPassed'],
                'createdAt': row_dict['createdAt']
            })
        
        return results
    
    def get_user_test_count(self, user_id: int) -> int:
        """Получить количество тестов пользователя"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM test_results WHERE userId = ?", (user_id,))
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def get_user_payments_count(self, user_id: int) -> int:
        """Получить количество оплаченных пересдач"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM payments 
            WHERE userId = ? AND status = 'completed'
        """, (user_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count

# Глобальный экземпляр базы данных
db = SimpleDB()