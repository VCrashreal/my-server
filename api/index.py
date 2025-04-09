import os
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# Путь к базе данных
DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

# Создание базы данных, если её нет
if not os.path.exists(DB_PATH):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password TEXT
                        )''')
        conn.commit()

# Модель пользователя
class User(BaseModel):
    username: str
    password: str

# Роуты
@app.get("/")
def read_root():
    return {"message": "Сервер работает!"}

@app.get("/ping")
def ping():
    return JSONResponse(content={"ping": "pong"})

@app.post("/register")
def register(user: User):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))
            conn.commit()
            return {"message": "Пользователь успешно зарегистрирован"}
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")

@app.post("/login")
def login(user: User):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user.username, user.password))
        result = cursor.fetchone()
        if result:
            return {"message": "Успешный вход"}
        else:
            raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")
