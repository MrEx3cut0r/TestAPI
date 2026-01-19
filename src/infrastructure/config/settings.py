# src/infrastructure/config/settings.py
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):    
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    
    POSTGRES_USER: str = "postgres"          
    POSTGRES_PASSWORD: str = "postgres"       
    POSTGRES_DB: str = "db"
    POSTGRES_HOST: str = "postgres"        
    POSTGRES_PORT: int = 5432
    
    REDIS_HOST: str = "redis"                
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    DERIBIT_API_URL: str = "https://www.deribit.com/api/v2"
    
    CELERY_BROKER_URL: str = Field(default="redis://redis:6379/0")
    CELERY_RESULT_BACKEND: str = Field(default="redis://redis:6379/0")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()