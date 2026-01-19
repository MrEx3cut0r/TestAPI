from dataclasses import dataclass
from typing import List, Optional, Any
from .price_dto import PriceDTO


@dataclass
class BaseResponse:
    
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    
    
@dataclass
class PriceListResponse:
    
    ticker: str
    prices: List[PriceDTO]
    count: int
    
    @classmethod
    def create(cls, ticker: str, prices: List[PriceDTO]) -> 'PriceListResponse':
        return cls(
            ticker=ticker,
            prices=prices,
            count=len(prices)
        )


@dataclass
class PriceResponse:
    
    ticker: str
    price: PriceDTO
    
    @classmethod
    def create(cls, ticker: str, price: PriceDTO) -> 'PriceResponse':
        return cls(ticker=ticker, price=price)