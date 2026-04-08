from sqlalchemy import Column, Date, DateTime, Integer, String, func

from app.core.database import Base


class Draw(Base):
    __tablename__ = "draws"

    id = Column(Integer, primary_key=True, index=True)
    draw_no = Column(String(50), unique=True, nullable=False, index=True)
    draw_date = Column(Date, nullable=False, index=True)
    n1 = Column(Integer, nullable=False)
    n2 = Column(Integer, nullable=False)
    n3 = Column(Integer, nullable=False)
    n4 = Column(Integer, nullable=False)
    n5 = Column(Integer, nullable=False)
    numbers_sorted = Column(String(50), nullable=False)
    source = Column(String(100), nullable=False, default="csv_import")
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    @property
    def numbers(self) -> list[int]:
        return [self.n1, self.n2, self.n3, self.n4, self.n5]
