from typing import List
from src.domain.ports.market_data_provider import MarketDataProvider
from src.domain.ports.price_repository import PriceRepository
from src.domain.entities.price import Price
from src.domain.value_objects.currency import CurrencyPair


class FetchMarketPricesUseCase:    
    def __init__(
        self, 
        market_data_provider: MarketDataProvider,
        price_repository: PriceRepository
    ):
        self.market_data_provider = market_data_provider
        self.price_repository = price_repository
    
    async def execute(self, tickers: List[str] = None) -> List[Price]:

        if tickers is None:
            tickers = CurrencyPair.list()
        
        prices_dict = await self.market_data_provider.get_index_prices(tickers)
        
        prices = list(prices_dict.values())
        
        if prices:
            saved_prices = await self.price_repository.batch_save(prices)
            return saved_prices
        
        return []