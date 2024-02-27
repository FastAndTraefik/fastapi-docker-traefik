from pydantic import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')


settings = Settings()
