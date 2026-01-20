from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.presentation.middleware.error_handler import ErrorHandlerMiddleware
from src.presentation.middleware.logging_middleware import LoggingMiddleware
from src.infrastructure.config.logging_config import setup_logging
from src.infrastructure.database.session import db_manager
from src.presentation.api.v1.prices import router as prices_router
import time

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    
    await db_manager.create_tables()

    yield
    


app = FastAPI(
    title="Crypto Price Tracker API",
    description="API для отслеживания цен криптовалют с биржи Deribit",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(LoggingMiddleware)

app.include_router(prices_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Crypto Price Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected", 
        "timestamp": int(time.time())
    }


@app.get("/info")
async def app_info():
    import src
    return {
        "app_name": "Crypto Price Tracker",
        "version": "1.0.0",
        "description": "Track cryptocurrency prices from Deribit exchange",
        "supported_tickers": ["btc_usd", "eth_usd"]
    }