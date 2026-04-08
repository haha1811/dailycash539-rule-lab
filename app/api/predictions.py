from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.prediction_service import run_latest_prediction

router = APIRouter(prefix="/api/predictions", tags=["predictions-api"])
ui_router = APIRouter(tags=["predictions-ui"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/latest")
def latest_prediction(db: Session = Depends(get_db)):
    return run_latest_prediction(db)


@ui_router.get("/predictions/latest", response_class=HTMLResponse)
def latest_prediction_page(request: Request, db: Session = Depends(get_db)):
    data = run_latest_prediction(db)
    return templates.TemplateResponse("prediction_latest.html", {"request": request, "data": data})
