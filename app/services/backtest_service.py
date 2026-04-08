import random
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.backtest_result import BacktestResult
from app.models.backtest_run import BacktestRun
from app.models.draw import Draw
from app.models.rule_config import RuleConfig
from app.rules import RULE_REGISTRY
from app.services.aggregator_service import aggregate_rule_outputs
from app.services.prediction_service import serialize_draw


def _hits(picked: list[int], actual: list[int]) -> int:
    return len(set(picked) & set(actual))


def _metric(hit_counts: list[int]) -> dict:
    total = len(hit_counts) or 1
    return {
        "total_draws": len(hit_counts),
        "avg_hit": round(sum(hit_counts) / total, 4),
        "hit_ge_1_ratio": round(sum(1 for h in hit_counts if h >= 1) / total, 4),
        "hit_ge_2_ratio": round(sum(1 for h in hit_counts if h >= 2) / total, 4),
        "hit_ge_3_ratio": round(sum(1 for h in hit_counts if h >= 3) / total, 4),
    }


def create_backtest(db: Session, payload: dict) -> BacktestRun:
    run = BacktestRun(**payload, status="running")
    db.add(run)
    db.commit()
    db.refresh(run)

    draws = (
        db.query(Draw)
        .filter(Draw.draw_date >= run.start_draw_date, Draw.draw_date <= run.end_draw_date)
        .order_by(Draw.draw_date.asc(), Draw.id.asc())
        .all()
    )
    enabled_rules = db.query(RuleConfig).filter(RuleConfig.is_enabled.is_(True)).all()
    weights = {r.rule_id: r.weight for r in enabled_rules}

    strategy_hits, random_hits, hot_hits, cold_hits = [], [], [], []

    for target_draw in draws:
        history_draws = (
            db.query(Draw)
            .filter(Draw.draw_date < target_draw.draw_date)
            .order_by(Draw.draw_date.asc(), Draw.id.asc())
            .all()
        )
        history = [serialize_draw(d) for d in history_draws]
        if not history:
            continue

        outputs = []
        for rc in enabled_rules:
            rule = RULE_REGISTRY.get(rc.rule_id)
            if rule:
                outputs.append(rule.evaluate(history, rc.params_json or {}))

        aggregate = aggregate_rule_outputs(outputs, weights)
        predicted = [row["number"] for row in aggregate[: run.top_k]]
        actual = target_draw.numbers
        hit_count = _hits(predicted, actual)
        strategy_hits.append(hit_count)

        hot_result = RULE_REGISTRY["hot_number_rule"].evaluate(history, {"window_size": 10, "top_n": 5})
        cold_result = RULE_REGISTRY["cold_number_rule"].evaluate(history, {"window_size": 15, "top_n": 5})
        random_pick = sorted(random.sample(range(1, 40), 5))

        hot_hits.append(_hits(hot_result["candidates"][: run.top_k], actual))
        cold_hits.append(_hits(cold_result["candidates"][: run.top_k], actual))
        random_hits.append(_hits(random_pick[: run.top_k], actual))

        row = BacktestResult(
            backtest_run_id=run.id,
            draw_id=target_draw.id,
            predicted_numbers=predicted,
            actual_numbers=actual,
            hit_count=hit_count,
            triggered_rules_json=outputs,
            score_map_json={str(r["number"]): r["final_score"] for r in aggregate},
        )
        db.add(row)

    summary = {
        "strategy": _metric(strategy_hits),
        "random_baseline": _metric(random_hits),
        "hot_baseline": _metric(hot_hits),
        "cold_baseline": _metric(cold_hits),
    }

    run.summary_json = summary
    run.status = "completed"
    run.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(run)
    return run
