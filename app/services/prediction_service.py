from sqlalchemy.orm import Session

from app.models.draw import Draw
from app.models.rule_config import RuleConfig
from app.rules import RULE_REGISTRY
from app.services.aggregator_service import aggregate_rule_outputs


def serialize_draw(draw: Draw) -> dict:
    return {"id": draw.id, "draw_date": draw.draw_date.isoformat(), "numbers": draw.numbers}


def run_latest_prediction(db: Session) -> dict:
    draws = db.query(Draw).order_by(Draw.draw_date.asc(), Draw.id.asc()).all()
    history = [serialize_draw(d) for d in draws]

    rule_configs = (
        db.query(RuleConfig)
        .filter(RuleConfig.is_enabled.is_(True))
        .order_by(RuleConfig.rule_id.asc())
        .all()
    )

    outputs = []
    weights = {}
    for rc in rule_configs:
        rule = RULE_REGISTRY.get(rc.rule_id)
        if not rule:
            continue
        result = rule.evaluate(history, rc.params_json or {})
        outputs.append(result)
        weights[rc.rule_id] = rc.weight

    final_numbers = aggregate_rule_outputs(outputs, weights)
    latest_date = draws[-1].draw_date.isoformat() if draws else None
    return {
        "base_draw_date": latest_date,
        "triggered_rules": outputs,
        "final_candidates": final_numbers,
    }
