from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from src.domain.entities.price import Price
from src.domain.value_objects.currency import Ticker
from src.domain.value_objects.timestamp import UnixTimestamp


@dataclass
class PriceDTO:
    
    id: Optional[int] = None
    ticker: str = ""
    price: float = 0.0
    timestamp: int = 0
    
    @classmethod
    def from_domain(cls, price: Price) -> 'PriceDTO':
        return cls(
            id=price.id,
            ticker=price.ticker,
            price=price.price,
            timestamp=price.timestamp
        )
    
    def to_domain(self) -> Price:
        return Price(
            id=self.id,
            ticker=self.ticker,
            price=self.price,
            timestamp=self.timestamp
        )
    
    @property
    def datetime(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp)
    
    @property
    def formatted_price(self) -> str:
        return f"${self.price:,.2f}"