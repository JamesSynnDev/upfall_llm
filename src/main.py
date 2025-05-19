import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.routes.chat import router as chat_router


# main.py 파일 기준으로 static 디렉토리 경로 계산
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app = FastAPI()
app.include_router(chat_router)


# 존재하지 않는 디렉토리를 마운트하면 에러가 나므로, 없으면 생성
if not os.path.isdir(STATIC_DIR):
    os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})
