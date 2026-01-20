import asyncio
import logging
from typing import List
from src.infrastructure.celery_app.worker import celery_app
from src.application.use_cases.fetch_market_prices_uc import FetchMarketPricesUseCase
from src.infrastructure.external.deribit_client import DeribitClient
from src.infrastructure.database.repositories.price_repository_impl import PriceRepositoryImpl
from src.infrastructure.database.session import db_manager
from src.infrastructure.config.settings import settings
from src.domain.value_objects.currency import CurrencyPair

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3)
def fetch_market_prices_task(self, tickers: List[str] = None):
    if tickers is None:
        tickers = CurrencyPair.list()
    
    try:        
        result = asyncio.run(async_fetch_prices(tickers))
        return result
        
    except Exception as e:
        logger.error(f"Price fetch task failed: {str(e)}")
        retry_count = self.request.retries
        countdown = 2 ** retry_count 
        
        raise self.retry(exc=e, countdown=countdown)


async def async_fetch_prices(tickers: List[str]):
    try:
        async for session in db_manager.get_session():
            deribit_client = DeribitClient(settings.DERIBIT_API_URL)
            price_repository = PriceRepositoryImpl(session)
            
            fetch_uc = FetchMarketPricesUseCase(
                market_data_provider=deribit_client,
                price_repository=price_repository
            )
            
            prices = await fetch_uc.execute(tickers)
            
            logger.info(f"Successfully fetched {len(prices)} prices")
            return {
                'success': True,
                'prices_fetched': len(prices) if prices else 0,
                'tickers': tickers
            }
    except Exception as e:
        logger.error(f"Error in async_fetch: {str(e)}")
        raise