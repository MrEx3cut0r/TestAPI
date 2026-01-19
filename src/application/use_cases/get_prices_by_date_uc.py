from datetime import datetime
from typing import List
from src.domain.ports.price_repository import PriceRepository
from src.application.dtos.price_dto import PriceDTO
from src.domain.exceptions.domain_exceptions import InvalidTickerException
from src.domain.value_objects.currency import CurrencyPair


class GetPricesByDateUseCase:    
    def __init__(self, price_repository: PriceRepository):
        self.price_repository = price_repository
    
    async def execute(
        self, 
        ticker: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[PriceDTO]:
        if ticker not in CurrencyPair.list():
            raise InvalidTickerException(
                f"Invalid ticker: {ticker}. Supported tickers: {CurrencyPair.list()}"
            )
        
        if start_date > end_date:
            raise ValueError("start_date cannot be greater than end_date")
        
        prices = await self.price_repository.get_by_date_range(
            ticker, start_date, end_date
        )
        
        return [PriceDTO.from_domain(price) for price in prices]