# 🚀 Task Tracker Server

сервер для управления задачами, построенный на **FastAPI** с использованием **PostgreSQL** и **SQLAlchemy**. Проект демонстрирует навыки backend-разработки, работу с базами данных, аутентификацией и контейнеризацией.

## 📌 Особенности проекта

- **FastAPI** – современный, быстрый веб-фреймворк для Python
- **PostgreSQL** – реляционная база данных
- **SQLAlchemy** – ORM для работы с БД
- **Pydantic** – валидация данных и сериализация
- **Docker** – контейнеризация приложения
- **JWT-аутентификация** – защита эндпоинтов
- **Асинхронная работа** – высокая производительность

## 🗂 Структура проекта

tracker-server/
├── app/
│ ├── init.py
│ ├── main.py # Точка входа, настройка FastAPI
│ ├── database.py # Подключение к БД, настройка сессии
│ ├── models.py # SQLAlchemy модели
│ ├── schemas.py # Pydantic схемы
│ ├── crud.py # Бизнес-логика (создание, чтение, обновление, удаление)
│ ├── auth.py # Логика аутентификации и JWT
│ └── dependencies.py # Зависимости (получение текущего пользователя)
├── .env.example # Пример переменных окружения
├── .gitignore
├── docker-compose.yml # Запуск приложения и БД через Docker
├── Dockerfile # Образ приложения
├── requirements.txt # Зависимости Python
└── README.md # Эта документация


## 🔧 Быстрый запуск

### 1. Клонирование репозитория
git clone https://github.com/Aleksey242424/tracker-server.git
cd tracker-server
### 2. Настройка переменных окружения
Создайте файл .env на основе примера:
cp .env.example .env
### 3. Содержимое env файла
DB_HOST=db
DB_PORT=5432
DB_NAME=tracker_db
DB_USER=postgres
DB_PASS=your_strong_password
SECRET_KEY=your_secret_JWT_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

🛠 Технические детали
Модели базы данных
User – пользователи системы (id, username, hashed_password)

Task – задачи (id, title, description, is_completed, user_id, created_at)

Зависимости проекта
Основные зависимости (полный список в requirements.txt):

fastapi==0.104.1

sqlalchemy==2.0.23

psycopg2-binary==2.9.9

python-jose[cryptography]==3.3.0

passlib[bcrypt]==1.7.4

python-dotenv==1.0.0
