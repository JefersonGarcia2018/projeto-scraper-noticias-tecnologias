import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.models.news import News
import logging

logger = logging.getLogger(__name__)

def scrape_g1_tecnologia(db: Session) -> int:
    url = "https://g1.globo.com/tecnologia/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Erro ao acessar {url}: {e}")
        return 0

    soup = BeautifulSoup(response.content, "html.parser")
    feed_items = soup.find_all("div", class_="feed-post")
    
    novas_noticias = 0
    
    for item in feed_items:
        try:
            # Extrair título a partir de .feed-post-body-title -> a
            title_tag = item.select_one(".feed-post-body-title a")
            # Extrair resumo a partir de .feed-post-body-resumo p
            summary_tag = item.select_one(".feed-post-body-resumo p")
            # Extrair link do título ou da imagem
            link_tag = item.select_one(".feed-post-link")
            # Extrair imagem
            img_tag = item.select_one(".bstn-fd-picture-image")
            # Extrair data de publicação
            date_tag = item.select_one(".feed-post-datetime")

            if not title_tag or not link_tag:
                continue
                
            title = title_tag.text.strip()
            link = link_tag.get("href")
            summary = summary_tag.text.strip() if summary_tag else None
            
            # G1 pode usar data-src ou src (ou atributos srcset)
            image_url = None
            if img_tag:
                image_url = img_tag.get("src") or img_tag.get("data-mrf-layout-img")

            published_date = date_tag.text.strip() if date_tag else None

            # Verificar se a notícia já existe no banco (via link único)
            existing_news = db.query(News).filter(News.link == link).first()
            if not existing_news:
                nova_noticia = News(
                    title=title,
                    summary=summary,
                    link=link,
                    image_url=image_url,
                    published_date=published_date
                )
                db.add(nova_noticia)
                db.commit()
                novas_noticias += 1
                
        except Exception as e:
            logger.error(f"Erro ao parsear notícia individual: {e}")
            db.rollback()

    return novas_noticias
