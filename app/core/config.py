from pydantic_settings import BaseSettings
from typing import List, Tuple

class Settings(BaseSettings):
    DATABASE_URL: str
    COUNTRY_COMBINATIONS: List[Tuple[str, str]]
    POOL_SIZE: int = 6
    
    class Config:
        env_file = ".env"

settings = Settings()