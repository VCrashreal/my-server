from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Vercel + FastAPI!"}

@app.get("/ping")
def ping():
    return JSONResponse(content={"ping": "pong"})
