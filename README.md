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


## 🔧 Быстрый запуск

### 1. Клонирование репозитория
git clone https://github.com/Aleksey242424/tracker-server.git
cd tracker-server
### 2. Настройка переменных окружения
Создайте файл .env на основе примера:
cp .env.example .env
### 3. Содержимое env файла
DB_HOST=db<br><br>
DB_PORT=5432<br><br>
DB_NAME=tracker_db<br><br>
DB_USER=postgres<br><br>
DB_PASS=your_strong_password<br><br>
SECRET_KEY=your_secret_JWT_key<br><br>
ALGORITHM=HS256<br><br>
ACCESS_TOKEN_EXPIRE_MINUTES=30<br><br>

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
