from typing import Optional
from src.domain.ports.price_repository import PriceRepository
from src.application.dtos.price_dto import PriceDTO
from src.domain.exceptions.domain_exceptions import InvalidTickerException
from src.domain.value_objects.currency import CurrencyPair


class GetLastPriceUseCase:    
    def __init__(self, price_repository: PriceRepository):
        self.price_repository = price_repository
    
    async def execute(self, ticker: str) -> Optional[PriceDTO]:
        if ticker not in CurrencyPair.list():
            raise InvalidTickerException(
                f"Invalid ticker: {ticker}. Supported tickers: {CurrencyPair.list()}"
            )
        
        price = await self.price_repository.get_last(ticker)
        
        if price:
            return PriceDTO.from_domain(price)
        return None