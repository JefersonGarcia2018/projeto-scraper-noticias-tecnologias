from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models.news import News
from app.schemas.news import NewsResponse
from app.services.scraper import scrape_g1_tecnologia
from app.ws.manager import manager
from app.api.v1.auth import require_admin

router = APIRouter()

@router.get("/", response_model=List[NewsResponse])
def get_news(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """Retorna as notícias cadastradas, ordenadas pela mais recente inserção/data"""
    noticias = db.query(News).order_by(News.id.desc()).offset(skip).limit(limit).all()
    return noticias

async def background_scraper(db: Session):
    novas_noticias = scrape_g1_tecnologia(db)
    if novas_noticias > 0:
        await manager.broadcast(f"Temos {novas_noticias} nova(s) notícia(s)! Atualize a página.")

@router.post("/scrape")
def trigger_scraper(background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_admin=Depends(require_admin)):
    """Inicia a varredura do G1 em background (Apenas Admin)"""
    background_tasks.add_task(background_scraper, db)
    return {"message": "Scraper iniciado no background. Você será notificado por WebSocket."}

@router.delete("/{news_id}")
def delete_news(news_id: int, db: Session = Depends(get_db), current_admin=Depends(require_admin)):
    """Deleta uma notícia pelo ID (Apenas Admin)"""
    from fastapi import HTTPException
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    db.delete(news)
    db.commit()
    return {"message": "Notícia excluída com sucesso"}
