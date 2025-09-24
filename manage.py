import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

from prisma import Prisma

async def add_question():
    """Интерактивное добавление вопроса"""
    print("=== Добавление нового вопроса ===\n")
    
    text = input("Введите текст вопроса: ").strip()
    option1 = input("Вариант A: ").strip()
    option2 = input("Вариант B: ").strip()
    option3 = input("Вариант C: ").strip()
    option4 = input("Вариант D: ").strip()
    
    while True:
        try:
            correct = int(input("Номер правильного ответа (1-4): "))
            if 1 <= correct <= 4:
                break
            else:
                print("Введите число от 1 до 4!")
        except ValueError:
            print("Введите корректное число!")
    
    # Подключение к БД
    prisma = Prisma()
    await prisma.connect()
    
    try:
        question = await prisma.question.create(data={
            "text": text,
            "option1": option1,
            "option2": option2,
            "option3": option3,
            "option4": option4,
            "correctAnswer": correct
        })
        
        print(f"\n✅ Вопрос успешно добавлен с ID: {question.id}")
        
    except Exception as e:
        print(f"\n❌ Ошибка при добавлении вопроса: {e}")
    finally:
        await prisma.disconnect()

async def list_questions():
    """Список всех вопросов"""
    prisma = Prisma()
    await prisma.connect()
    
    try:
        questions = await prisma.question.find_many(
            order_by={"id": "asc"}
        )
        
        print(f"\n=== Всего вопросов: {len(questions)} ===\n")
        
        for q in questions:
            print(f"ID: {q.id}")
            print(f"Вопрос: {q.text}")
            print(f"A) {q.option1}")
            print(f"B) {q.option2}")
            print(f"C) {q.option3}")
            print(f"D) {q.option4}")
            print(f"Правильный ответ: {['A', 'B', 'C', 'D'][q.correctAnswer - 1]}")
            print("-" * 50)
        
    except Exception as e:
        print(f"❌ Ошибка при получении вопросов: {e}")
    finally:
        await prisma.disconnect()

async def delete_question():
    """Удаление вопроса"""
    await list_questions()
    
    try:
        question_id = int(input("\nВведите ID вопроса для удаления: "))
    except ValueError:
        print("❌ Неверный ID!")
        return
    
    prisma = Prisma()
    await prisma.connect()
    
    try:
        question = await prisma.question.find_unique(
            where={"id": question_id}
        )
        
        if not question:
            print("❌ Вопрос не найден!")
            return
        
        # Показываем вопрос
        print(f"\nВопрос для удаления:")
        print(f"ID: {question.id}")
        print(f"Текст: {question.text}")
        
        confirm = input("\nВы уверены? (y/N): ").strip().lower()
        if confirm in ['y', 'yes', 'да']:
            await prisma.question.delete(where={"id": question_id})
            print("✅ Вопрос успешно удален!")
        else:
            print("Отменено.")
            
    except Exception as e:
        print(f"❌ Ошибка при удалении вопроса: {e}")
    finally:
        await prisma.disconnect()

async def show_stats():
    """Статистика базы данных"""
    prisma = Prisma()
    await prisma.connect()
    
    try:
        questions_count = await prisma.question.count()
        users_count = await prisma.user.count()
        tests_count = await prisma.test.count()
        results_count = await prisma.testresult.count()
        payments_count = await prisma.payment.count()
        
        print("\n=== Статистика базы данных ===")
        print(f"Вопросов: {questions_count}")
        print(f"Пользователей: {users_count}")
        print(f"Тестов: {tests_count}")
        print(f"Результатов: {results_count}")
        print(f"Платежей: {payments_count}")
        
        if results_count > 0:
            passed_count = await prisma.testresult.count(
                where={"isPassed": True}
            )
            pass_rate = (passed_count / results_count) * 100
            print(f"Процент прохождения: {pass_rate:.1f}%")
        
    except Exception as e:
        print(f"❌ Ошибка при получении статистики: {e}")
    finally:
        await prisma.disconnect()

async def main():
    """Главное меню"""
    while True:
        print("\n" + "=" * 50)
        print("УПРАВЛЕНИЕ QUIZ APP")
        print("=" * 50)
        print("1. Добавить вопрос")
        print("2. Показать все вопросы")
        print("3. Удалить вопрос")
        print("4. Статистика")
        print("5. Выход")
        print("-" * 50)
        
        choice = input("Выберите действие (1-5): ").strip()
        
        if choice == '1':
            await add_question()
        elif choice == '2':
            await list_questions()
        elif choice == '3':
            await delete_question()
        elif choice == '4':
            await show_stats()
        elif choice == '5':
            print("До свидания!")
            break
        else:
            print("❌ Неверный выбор!")
        
        input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    asyncio.run(main())