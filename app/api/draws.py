from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.draw import Draw
from app.services.draw_import_service import import_draws_csv

router = APIRouter(prefix="/api/draws", tags=["draws-api"])
ui_router = APIRouter(tags=["draws-ui"])
templates = Jinja2Templates(directory="app/templates")


@router.post("/import")
async def import_draws(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = (await file.read()).decode("utf-8")
    return import_draws_csv(db, content, source=file.filename or "upload")


@ui_router.get("/draws", response_class=HTMLResponse)
def draws_page(request: Request, db: Session = Depends(get_db)):
    total = db.query(Draw).count()
    recent = db.query(Draw).order_by(Draw.draw_date.desc(), Draw.id.desc()).limit(20).all()
    return templates.TemplateResponse("draws.html", {"request": request, "total": total, "recent": recent})


@ui_router.get("/draws/import", response_class=HTMLResponse)
def import_page(request: Request):
    return templates.TemplateResponse("draw_import.html", {"request": request})
