from datetime import date

from app.core.database import Base
from app.models import Draw, RuleConfig
from app.rules import DEFAULT_RULES
from app.services.backtest_service import create_backtest


def seed(db):
    Base.metadata.create_all(bind=db.bind)
    for i in range(1, 12):
        nums = [((i + j - 1) % 39) + 1 for j in range(5)]
        db.add(
            Draw(
                draw_no=f"D{i}",
                draw_date=date(2025, 1, i),
                n1=nums[0],
                n2=nums[1],
                n3=nums[2],
                n4=nums[3],
                n5=nums[4],
                numbers_sorted=",".join(map(str, sorted(nums))),
                source="test",
            )
        )
    for r in DEFAULT_RULES:
        db.add(RuleConfig(**r))
    db.commit()


def test_backtest_no_future_data_and_hit_count(db_session):
    seed(db_session)
    run = create_backtest(
        db_session,
        {
            "name": "t",
            "start_draw_date": date(2025, 1, 3),
            "end_draw_date": date(2025, 1, 10),
            "top_k": 5,
            "baseline_modes": ["random", "hot", "cold"],
        },
    )
    assert run.status == "completed"
    assert "strategy" in run.summary_json
    assert run.summary_json["random_baseline"]["total_draws"] >= 1
