from abc import ABC, abstractmethod
from typing import Dict
from ..entities.price import Price


class MarketDataProvider(ABC):
    @abstractmethod
    async def get_index_price(self, ticker: str) -> Price:
        pass
    
    @abstractmethod
    async def get_index_prices(self, tickers: list) -> Dict[str, Price]:
        pass