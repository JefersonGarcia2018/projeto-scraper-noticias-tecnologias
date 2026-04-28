from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.middleware import RequestLoggingMiddleware
from app.database.session import engine, SessionLocal
from app.database.base import Base
from app.models.user import User
from app.core.security import get_password_hash

from app.api.v1 import auth, users, news
from app.ws.manager import manager

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@tecnologia.com",
            hashed_password=get_password_hash("admin123"),
            role="admin"
        )
        db.add(admin)
        db.commit()
    db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lógica de inicialização
    print("Iniciando a aplicação... Criando tabelas e seed.")
    init_db()
    yield
    # Lógica de finalização
    print("Finalizando a aplicação...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para o projeto de Notícias e Tecnologias",
    version=settings.VERSION,
    lifespan=lifespan
)

# Configuração de CORS
origins = [
    "http://localhost:9000",
    "http://127.0.0.1:9000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(news.router, prefix=f"{settings.API_V1_STR}/news", tags=["news"])

@app.websocket("/ws/news")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # O WebSocket precisa ficar aguardando mensagens para não fechar, 
            # mesmo que a comunicação aqui primária seja server->client.
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de Notícias e Tecnologias! Acesse /docs para a doc Swagger."}
