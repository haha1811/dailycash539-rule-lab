import json

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.rule_config import RuleConfig
from app.schemas.common import RuleUpdate

router = APIRouter(prefix="/api/rules", tags=["rules-api"])
ui_router = APIRouter(tags=["rules-ui"])
templates = Jinja2Templates(directory="app/templates")


@router.get("")
def list_rules(db: Session = Depends(get_db)):
    return db.query(RuleConfig).order_by(RuleConfig.rule_id.asc()).all()


@router.put("/{rule_id}")
def update_rule(rule_id: str, payload: RuleUpdate, db: Session = Depends(get_db)):
    row = db.query(RuleConfig).filter(RuleConfig.rule_id == rule_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Rule not found")
    row.is_enabled = payload.is_enabled
    row.params_json = payload.params_json
    row.weight = payload.weight
    db.commit()
    db.refresh(row)
    return row


@ui_router.get("/rules", response_class=HTMLResponse)
def rules_page(request: Request, db: Session = Depends(get_db)):
    rows = db.query(RuleConfig).order_by(RuleConfig.rule_id.asc()).all()
    return templates.TemplateResponse("rules.html", {"request": request, "rules": rows})


@ui_router.post("/rules/{rule_id}")
def update_rule_form(
    rule_id: str,
    is_enabled: str = Form("false"),
    weight: float = Form(...),
    params_json: str = Form("{}"),
    db: Session = Depends(get_db),
):
    row = db.query(RuleConfig).filter(RuleConfig.rule_id == rule_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Rule not found")
    row.is_enabled = is_enabled == "on"
    row.weight = weight
    row.params_json = json.loads(params_json or "{}")
    db.commit()
    return RedirectResponse(url="/rules", status_code=303)
