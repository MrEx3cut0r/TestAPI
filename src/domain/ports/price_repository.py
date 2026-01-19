from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from ..entities.price import Price


class PriceRepository(ABC):
    
    @abstractmethod
    async def save(self, price: Price) -> Price:
        pass
    
    @abstractmethod
    async def get_all(self, ticker: str) -> List[Price]:
        pass
    
    @abstractmethod
    async def get_last(self, ticker: str) -> Optional[Price]:
        pass
    
    @abstractmethod
    async def get_by_date_range(
        self, 
        ticker: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Price]:
        pass
    
    @abstractmethod
    async def batch_save(self, prices: List[Price]) -> List[Price]:
        pass