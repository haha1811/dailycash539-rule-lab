from datetime import date, datetime
from pydantic import BaseModel


class DrawOut(BaseModel):
    id: int
    draw_no: str
    draw_date: date
    n1: int
    n2: int
    n3: int
    n4: int
    n5: int
    numbers_sorted: str
    source: str
    created_at: datetime

    class Config:
        from_attributes = True


class RuleOut(BaseModel):
    rule_id: str
    name: str
    description: str
    is_enabled: bool
    params_json: dict
    weight: float

    class Config:
        from_attributes = True


class RuleUpdate(BaseModel):
    is_enabled: bool
    params_json: dict
    weight: float


class BacktestCreate(BaseModel):
    name: str
    start_draw_date: date
    end_draw_date: date
    top_k: int = 5
    baseline_modes: list[str] = ["random", "hot", "cold"]
