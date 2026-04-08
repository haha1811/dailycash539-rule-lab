from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "dailycash539-rule-lab")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./dailycash539.db")


settings = Settings()
