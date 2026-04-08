from sqlalchemy import Column, Date, DateTime, Integer, JSON, String, func

from app.core.database import Base


class BacktestRun(Base):
    __tablename__ = "backtest_runs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    start_draw_date = Column(Date, nullable=False)
    end_draw_date = Column(Date, nullable=False)
    top_k = Column(Integer, nullable=False, default=5)
    baseline_modes = Column(JSON, nullable=False, default=list)
    status = Column(String(50), nullable=False, default="pending")
    summary_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
