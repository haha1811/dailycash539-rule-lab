from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.backtests import router as backtests_api_router
from app.api.backtests import ui_router as backtests_ui_router
from app.api.draws import router as draws_api_router
from app.api.draws import ui_router as draws_ui_router
from app.api.predictions import router as predictions_api_router
from app.api.predictions import ui_router as predictions_ui_router
from app.api.rules import router as rules_api_router
from app.api.rules import ui_router as rules_ui_router
from app.core.database import Base, engine, get_db
from app.models import BacktestResult, BacktestRun, Draw, RuleConfig
from app.rules import DEFAULT_RULES

app = FastAPI(title="dailycash539-rule-lab")
templates = Jinja2Templates(directory="app/templates")

Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def seed_rules() -> None:
    db = next(get_db())
    try:
        for item in DEFAULT_RULES:
            exists = db.query(RuleConfig).filter(RuleConfig.rule_id == item["rule_id"]).first()
            if not exists:
                db.add(RuleConfig(**item))
        db.commit()
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    stats = {
        "draw_count": db.query(Draw).count(),
        "rule_count": db.query(RuleConfig).count(),
        "backtest_count": db.query(BacktestRun).count(),
    }
    return templates.TemplateResponse("index.html", {"request": request, "stats": stats})


app.include_router(draws_api_router)
app.include_router(rules_api_router)
app.include_router(predictions_api_router)
app.include_router(backtests_api_router)

app.include_router(draws_ui_router)
app.include_router(rules_ui_router)
app.include_router(predictions_ui_router)
app.include_router(backtests_ui_router)
