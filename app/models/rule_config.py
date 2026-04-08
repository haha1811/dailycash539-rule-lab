from sqlalchemy import Boolean, Column, DateTime, Float, Integer, JSON, String, func

from app.core.database import Base


class RuleConfig(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    is_enabled = Column(Boolean, nullable=False, default=True)
    params_json = Column(JSON, nullable=False, default=dict)
    weight = Column(Float, nullable=False, default=1.0)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
