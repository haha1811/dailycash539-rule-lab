from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class BacktestResult(Base):
    __tablename__ = "backtest_results"

    id = Column(Integer, primary_key=True, index=True)
    backtest_run_id = Column(Integer, ForeignKey("backtest_runs.id"), nullable=False, index=True)
    draw_id = Column(Integer, ForeignKey("draws.id"), nullable=False, index=True)
    predicted_numbers = Column(JSON, nullable=False)
    actual_numbers = Column(JSON, nullable=False)
    hit_count = Column(Integer, nullable=False)
    triggered_rules_json = Column(JSON, nullable=False)
    score_map_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    run = relationship("BacktestRun")
