import logging
from typing import List
from src.domain.entities.price import Price
from src.application.use_cases.fetch_market_prices_uc import FetchMarketPricesUseCase
from src.domain.value_objects.currency import CurrencyPair

logger = logging.getLogger(__name__)

class PriceFetchService:    
    def __init__(self, fetch_market_prices_uc: FetchMarketPricesUseCase):
        self.fetch_market_prices_uc = fetch_market_prices_uc
    
    async def fetch_all_prices(self) -> List[Price]:
        try:
            prices = await self.fetch_market_prices_uc.execute()
            return prices
        except Exception as e:
            logger.error(f"Error fetching prices: {str(e)}")
            raise
    
    async def fetch_prices_for_tickers(self, tickers: List[str]) -> List[Price]:
        try:
            prices = await self.fetch_market_prices_uc.execute(tickers)
            return prices
        except Exception as e:
            logger.error(f"Error fetching prices: {str(e)}")
            raise