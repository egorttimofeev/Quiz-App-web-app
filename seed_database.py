import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

from simple_db import db

# Примеры вопросов для заполнения базы данных
SAMPLE_QUESTIONS = [
    {
        "text": "Какой язык программирования используется для создания веб-страниц?",
        "option1": "Python",
        "option2": "JavaScript",
        "option3": "C++", 
        "option4": "Java",
        "correctAnswer": 2
    },
    {
        "text": "Что означает аббревиатура HTML?",
        "option1": "HyperText Markup Language",
        "option2": "High Tech Modern Language",
        "option3": "Home Tool Markup Language",
        "option4": "Hyperlink and Text Markup Language",
        "correctAnswer": 1
    },
    {
        "text": "Какой HTTP-статус код означает 'Не найдено'?",
        "option1": "200",
        "option2": "301",
        "option3": "404",
        "option4": "500",
        "correctAnswer": 3
    },
    {
        "text": "Что такое API?",
        "option1": "Application Programming Interface",
        "option2": "Advanced Programming Instructions",
        "option3": "Automated Program Integration",
        "option4": "Application Protocol Interface",
        "correctAnswer": 1
    },
    {
        "text": "Какой тег используется для создания ссылки в HTML?",
        "option1": "<link>",
        "option2": "<a>",
        "option3": "<href>",
        "option4": "<url>",
        "correctAnswer": 2
    },
    {
        "text": "Что такое CSS?",
        "option1": "Computer Style Sheets",
        "option2": "Creative Style Sheets",
        "option3": "Cascading Style Sheets",
        "option4": "Colorful Style Sheets",
        "correctAnswer": 3
    },
    {
        "text": "Какой метод HTTP используется для получения данных?",
        "option1": "POST",
        "option2": "GET",
        "option3": "PUT",
        "option4": "DELETE",
        "correctAnswer": 2
    },
    {
        "text": "Что означает JSON?",
        "option1": "JavaScript Object Notation",
        "option2": "Java Syntax Object Notation",
        "option3": "JavaScript Output Network",
        "option4": "Java Script Online Notation",
        "correctAnswer": 1
    },
    {
        "text": "Какая база данных является реляционной?",
        "option1": "MongoDB",
        "option2": "Redis",
        "option3": "PostgreSQL",
        "option4": "Cassandra",
        "correctAnswer": 3
    },
    {
        "text": "Что такое Git?",
        "option1": "Система контроля версий",
        "option2": "Язык программирования",
        "option3": "Веб-сервер",
        "option4": "База данных",
        "correctAnswer": 1
    },
    {
        "text": "Какой тег используется для подключения CSS к HTML?",
        "option1": "<style>",
        "option2": "<css>",
        "option3": "<link>",
        "option4": "<stylesheet>",
        "correctAnswer": 3
    },
    {
        "text": "Что означает AJAX?",
        "option1": "Asynchronous JavaScript and XML",
        "option2": "Advanced JavaScript and XML",
        "option3": "Automatic JavaScript and XML",
        "option4": "Animated JavaScript and XML",
        "correctAnswer": 1
    },
    {
        "text": "Какой символ используется для комментариев в JavaScript?",
        "option1": "#",
        "option2": "//",
        "option3": "<!--",
        "option4": "%",
        "correctAnswer": 2
    },
    {
        "text": "Что такое DOM?",
        "option1": "Document Object Model",
        "option2": "Data Object Management",
        "option3": "Dynamic Object Method",
        "option4": "Digital Object Model",
        "correctAnswer": 1
    },
    {
        "text": "Какой порт по умолчанию использует HTTP?",
        "option1": "21",
        "option2": "80",
        "option3": "443",
        "option4": "8080",
        "correctAnswer": 2
    },
    {
        "text": "Что такое SQL?",
        "option1": "Structured Query Language",
        "option2": "Standard Query Language",
        "option3": "Simple Query Language",
        "option4": "Secure Query Language",
        "correctAnswer": 1
    },
    {
        "text": "Какой тег используется для создания таблицы в HTML?",
        "option1": "<table>",
        "option2": "<tab>",
        "option3": "<grid>",
        "option4": "<data>",
        "correctAnswer": 1
    },
    {
        "text": "Что означает URL?",
        "option1": "Universal Resource Locator",
        "option2": "Uniform Resource Locator",
        "option3": "Universal Reference Link",
        "option4": "Uniform Reference Locator",
        "correctAnswer": 2
    },
    {
        "text": "Какой язык программирования создал Гвидо ван Россум?",
        "option1": "Java",
        "option2": "Python",
        "option3": "C++",
        "option4": "JavaScript",
        "correctAnswer": 2
    },
    {
        "text": "Что такое Bootstrap?",
        "option1": "Язык программирования",
        "option2": "База данных",
        "option3": "CSS фреймворк",
        "option4": "Веб-сервер",
        "correctAnswer": 3
    },
    {
        "text": "Какой тег используется для создания списка в HTML?",
        "option1": "<list>",
        "option2": "<ul> или <ol>",
        "option3": "<menu>",
        "option4": "<items>",
        "correctAnswer": 2
    },
    {
        "text": "Что означает HTTPS?",
        "option1": "HyperText Transfer Protocol Secure",
        "option2": "HyperText Transfer Protocol System",
        "option3": "High Transfer Protocol Secure",
        "option4": "HyperText Transmission Protocol Secure",
        "correctAnswer": 1
    },
    {
        "text": "Какой оператор используется для сравнения в JavaScript?",
        "option1": "=",
        "option2": "==",
        "option3": "===",
        "option4": "Все варианты верны",
        "correctAnswer": 3
    },
    {
        "text": "Что такое Node.js?",
        "option1": "Библиотека JavaScript",
        "option2": "Среда выполнения JavaScript",
        "option3": "Фреймворк CSS",
        "option4": "База данных",
        "correctAnswer": 2
    },
    {
        "text": "Какой тег используется для создания формы в HTML?",
        "option1": "<form>",
        "option2": "<input>",
        "option3": "<field>",
        "option4": "<data>",
        "correctAnswer": 1
    },
    {
        "text": "Что означает MVC?",
        "option1": "Model View Controller",
        "option2": "Multiple View Control",
        "option3": "Modern View Component",
        "option4": "Master View Controller",
        "correctAnswer": 1
    },
    {
        "text": "Какой метод HTTP используется для отправки данных?",
        "option1": "GET",
        "option2": "POST",
        "option3": "PUT", 
        "option4": "OPTIONS",
        "correctAnswer": 2
    },
    {
        "text": "Что такое React?",
        "option1": "Язык программирования",
        "option2": "JavaScript библиотека",
        "option3": "База данных",
        "option4": "Веб-сервер",
        "correctAnswer": 2
    },
    {
        "text": "Какой тег используется для подключения JavaScript к HTML?",
        "option1": "<javascript>",
        "option2": "<js>",
        "option3": "<script>",
        "option4": "<code>",
        "correctAnswer": 3
    },
    {
        "text": "Что означает REST?",
        "option1": "Representational State Transfer",
        "option2": "Remote State Transfer",
        "option3": "Real State Transfer",
        "option4": "Reliable State Transfer",
        "correctAnswer": 1
    },
    {
        "text": "Какой символ используется для селекторов класса в CSS?",
        "option1": "#",
        "option2": ".",
        "option3": "@",
        "option4": "&",
        "correctAnswer": 2
    },
    {
        "text": "Что такое Docker?",
        "option1": "Язык программирования",
        "option2": "Платформа контейнеризации",
        "option3": "База данных",
        "option4": "Веб-фреймворк",
        "correctAnswer": 2
    },
    {
        "text": "Какой тег используется для создания заголовка в HTML?",
        "option1": "<header>",
        "option2": "<title>",
        "option3": "<h1>",
        "option4": "<head>",
        "correctAnswer": 3
    },
    {
        "text": "Что означает NPM?",
        "option1": "Node Package Manager",
        "option2": "New Package Manager",
        "option3": "Network Package Manager",
        "option4": "Node Program Manager",
        "correctAnswer": 1
    },
    {
        "text": "Какой символ используется для комментариев в CSS?",
        "option1": "//",
        "option2": "/* */",
        "option3": "#",
        "option4": "<!--",
        "correctAnswer": 2
    },
    {
        "text": "Что такое MongoDB?",
        "option1": "Реляционная база данных",
        "option2": "NoSQL база данных",
        "option3": "Язык программирования",
        "option4": "Веб-фреймворк",
        "correctAnswer": 2
    },
    {
        "text": "Какой тег используется для создания изображения в HTML?",
        "option1": "<image>",
        "option2": "<img>",
        "option3": "<pic>",
        "option4": "<photo>",
        "correctAnswer": 2
    },
    {
        "text": "Что означает SEO?",
        "option1": "Search Engine Optimization",
        "option2": "Secure Engine Operations",
        "option3": "System Engine Operations",
        "option4": "Search Error Optimization",
        "correctAnswer": 1
    },
    {
        "text": "Какой язык используется для стилизации веб-страниц?",
        "option1": "HTML",
        "option2": "JavaScript",
        "option3": "CSS",
        "option4": "PHP",
        "correctAnswer": 3
    },
    {
        "text": "Что такое Webpack?",
        "option1": "Библиотека JavaScript",
        "option2": "Сборщик модулей",
        "option3": "База данных",
        "option4": "Веб-сервер",
        "correctAnswer": 2
    },
    {
        "text": "Какой тег используется для создания параграфа в HTML?",
        "option1": "<paragraph>",
        "option2": "<p>",
        "option3": "<text>",
        "option4": "<par>",
        "correctAnswer": 2
    },
    {
        "text": "Что означает CDN?",
        "option1": "Content Delivery Network",
        "option2": "Central Data Network",
        "option3": "Computer Data Network",
        "option4": "Content Distribution Node",
        "correctAnswer": 1
    },
    {
        "text": "Какой символ используется для селекторов ID в CSS?",
        "option1": ".",
        "option2": "#",
        "option3": "@",
        "option4": "&",
        "correctAnswer": 2
    },
    {
        "text": "Что такое Vue.js?",
        "option1": "Язык программирования",
        "option2": "JavaScript фреймворк",
        "option3": "База данных",
        "option4": "CSS препроцессор",
        "correctAnswer": 2
    },
    {
        "text": "Какой порт по умолчанию использует HTTPS?",
        "option1": "80",
        "option2": "443",
        "option3": "8080",
        "option4": "3000",
        "correctAnswer": 2
    },
    {
        "text": "Что означает CRUD?",
        "option1": "Create Read Update Delete",
        "option2": "Control Read Update Deploy",
        "option3": "Create Retrieve Update Delete",
        "option4": "Control Retrieve Upload Deploy",
        "correctAnswer": 1
    },
    {
        "text": "Какой тег используется для создания кнопки в HTML?",
        "option1": "<btn>",
        "option2": "<button>",
        "option3": "<click>",
        "option4": "<input>",
        "correctAnswer": 2
    },
    {
        "text": "Что такое Sass?",
        "option1": "JavaScript библиотека",
        "option2": "CSS препроцессор",
        "option3": "База данных",
        "option4": "HTML фреймворк",
        "correctAnswer": 2
    },
    {
        "text": "Какой тип данных используется для хранения текста в JavaScript?",
        "option1": "text",
        "option2": "string",
        "option3": "char",
        "option4": "varchar",
        "correctAnswer": 2
    },
    {
        "text": "Что означает SPA?",
        "option1": "Single Page Application",
        "option2": "Secure Page Application",
        "option3": "Simple Page Application",
        "option4": "Static Page Application",
        "correctAnswer": 1
    },
    {
        "text": "Какой тег используется для создания видео в HTML5?",
        "option1": "<movie>",
        "option2": "<video>",
        "option3": "<media>",
        "option4": "<film>",
        "correctAnswer": 2
    }
]

def seed_database():
    """Заполнение базы данных примерами вопросов"""
    print("Инициализация базы данных...")
    
    try:
        # Добавление новых вопросов
        print(f"Добавление {len(SAMPLE_QUESTIONS)} вопросов...")
        
        for i, question_data in enumerate(SAMPLE_QUESTIONS, 1):
            db.create_question(
                text=question_data["text"],
                option1=question_data["option1"],
                option2=question_data["option2"],
                option3=question_data["option3"],
                option4=question_data["option4"],
                correct_answer=question_data["correctAnswer"]
            )
            print(f"Добавлен вопрос {i}/{len(SAMPLE_QUESTIONS)}")
        
        print("✅ База данных успешно заполнена!")
        
        # Проверка количества вопросов
        count = db.get_questions_count()
        print(f"Общее количество вопросов в базе: {count}")
        
    except Exception as e:
        print(f"❌ Ошибка при заполнении базы данных: {e}")

if __name__ == "__main__":
    seed_database()