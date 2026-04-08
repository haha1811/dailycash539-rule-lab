from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.backtest_result import BacktestResult
from app.models.backtest_run import BacktestRun
from app.schemas.common import BacktestCreate
from app.services.backtest_service import create_backtest

router = APIRouter(prefix="/api/backtests", tags=["backtests-api"])
ui_router = APIRouter(tags=["backtests-ui"])
templates = Jinja2Templates(directory="app/templates")


@router.post("")
def create_backtest_api(payload: BacktestCreate, db: Session = Depends(get_db)):
    return create_backtest(db, payload.model_dump())


@router.get("")
def list_backtests(db: Session = Depends(get_db)):
    return db.query(BacktestRun).order_by(BacktestRun.id.desc()).all()


@router.get("/{run_id}")
def get_backtest(run_id: int, db: Session = Depends(get_db)):
    run = db.query(BacktestRun).filter(BacktestRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Backtest run not found")
    return run


@router.get("/{run_id}/results")
def get_backtest_results(run_id: int, db: Session = Depends(get_db)):
    return db.query(BacktestResult).filter(BacktestResult.backtest_run_id == run_id).all()


@ui_router.get("/backtests", response_class=HTMLResponse)
def backtests_page(request: Request, db: Session = Depends(get_db)):
    runs = db.query(BacktestRun).order_by(BacktestRun.id.desc()).all()
    return templates.TemplateResponse("backtests.html", {"request": request, "runs": runs})
