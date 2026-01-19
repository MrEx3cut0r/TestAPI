import asyncio
import logging
from typing import List
from src.infrastructure.celery_app.worker import celery_app
from src.application.use_cases.fetch_market_prices_uc import FetchMarketPricesUseCase
from src.domain.ports.market_data_provider import MarketDataProvider
from src.domain.ports.price_repository import PriceRepository
from src.infrastructure.external.deribit_client import DeribitClient
from src.infrastructure.database.repositories.price_repository_impl import PriceRepositoryImpl
from src.infrastructure.database.session import db_manager
from src.infrastructure.config.settings import settings
from src.domain.value_objects.currency import CurrencyPair

logger = logging.getLogger(__name__)


def create_dependencies():
    deribit_client = DeribitClient(settings.DERIBIT_API_URL)
    
    return {
        'market_data_provider': deribit_client,
    }


@celery_app.task(bind=True, max_retries=3)
def fetch_market_prices_task(self, tickers: List[str] = None):
    if tickers is None:
        tickers = CurrencyPair.list()
    
    try:        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def async_fetch():
            try:
                async for session in db_manager.get_session():
                    deribit_client = DeribitClient(settings.DERIBIT_API_URL)
                    price_repository = PriceRepositoryImpl(session)
                    
                    fetch_uc = FetchMarketPricesUseCase(
                        market_data_provider=deribit_client,
                        price_repository=price_repository
                    )
                    
                    prices = await fetch_uc.execute(tickers)
                    
                    return prices
            except Exception as e:
                logger.error(f"Error in async_fetch: {str(e)}")
                raise
        
        result = loop.run_until_complete(async_fetch())
        loop.close()
        
        return {
            'success': True,
            'prices_fetched': len(result) if result else 0,
            'tickers': tickers
        }
        
    except Exception as e:
        logger.error(f"Price fetch task failed: {str(e)}")
        
        retry_count = self.request.retries
        countdown = 2 ** retry_count  
        
        raise self.retry(exc=e, countdown=countdown)


@celery_app.task
def test_task():
    return "Test task completed"