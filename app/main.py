from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import share

app = FastAPI()

# ★ CORS を追加（React → FastAPI の通信を許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 必要なら ["http://localhost:5173"] に変更可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(share.router)


