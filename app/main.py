from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, FileResponse
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import URL
from app.schemas import URLCreateRequest, URLResponse
from app.shortener import create_unique_short_code
from app.cache import get_cached_url, set_cached_url

# Cria as tabelas no banco caso ainda não existam.
# Em um cenário mais avançado isso seria feito via migrations (ex: Alembic).
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Encurtador de URLs", version="1.0.0")

STATIC_DIR = Path(__file__).resolve().parent / "static"


@app.get("/")
def serve_frontend():
    """Serve a página HTML simples do encurtador."""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health_check():
    """Endpoint simples para checar se a aplicação está de pé (usado pelo CI/monitoramento)."""
    return {"status": "ok"}


@app.post("/shorten", response_model=URLResponse)
def shorten_url(payload: URLCreateRequest, request: Request, db: Session = Depends(get_db)):
    """Recebe uma URL longa e retorna um código curto para acessá-la."""
    short_code = create_unique_short_code(db)

    url_entry = URL(short_code=short_code, original_url=str(payload.url))
    db.add(url_entry)
    db.commit()
    db.refresh(url_entry)

    # Já deixa no cache, já que acabou de ser criada (provável acesso em breve)
    set_cached_url(short_code, url_entry.original_url)

    base_url = str(request.base_url).rstrip("/")
    return URLResponse(
        short_code=url_entry.short_code,
        original_url=url_entry.original_url,
        short_url=f"{base_url}/{url_entry.short_code}",
    )


@app.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    """Redireciona do código curto para a URL original, usando cache antes do banco."""
    cached_url = get_cached_url(short_code)
    if cached_url:
        return RedirectResponse(url=cached_url)

    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="Código não encontrado")

    url_entry.access_count += 1
    db.commit()

    set_cached_url(short_code, url_entry.original_url)
    return RedirectResponse(url=url_entry.original_url)
