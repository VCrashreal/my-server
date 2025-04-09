from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()


# Создание базы данных, если её нет
DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')
if not os.path.exists(DB_PATH):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password TEXT
                        )''')
        conn.commit()


# Модель для входящих данных
class User(BaseModel):
    username: str
    password: str


@app.get("/")
def read_root():
    return {"message": "Сервер работает!"}


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