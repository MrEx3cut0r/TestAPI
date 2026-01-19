import aiohttp
import logging
from typing import Dict
from datetime import datetime
from src.domain.ports.market_data_provider import MarketDataProvider
from src.domain.entities.price import Price
from src.domain.value_objects.currency import CurrencyPair
from .aiohttp_client import AioHttpClient

logger = logging.getLogger(__name__)


class DeribitClient(MarketDataProvider):    
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.http_client = AioHttpClient(base_url=api_url)
    
    async def get_index_price(self, ticker: str) -> Price:
        if ticker not in CurrencyPair.list():
            raise ValueError(f"Unsupported ticker: {ticker}")
        
        deribit_ticker = ticker.replace('_', '-').upper()
        
        try:
            async with self.http_client as client:
                response = await client.get(
                    "public/get_index_price",
                    params={"index_name": deribit_ticker}
                )
                
                result = response.get("result", {})
                price = float(result.get("index_price", 0))
                timestamp = int(datetime.now().timestamp())
                
                if price <= 0:
                    raise ValueError(f"Invalid price received: {price}")
                
                return Price(
                    ticker=ticker,
                    price=price,
                    timestamp=timestamp
                )
                
        except Exception as e:
            logger.error(f"Failed to get index price for {ticker}: {str(e)}")
            raise RuntimeError(f"Failed to fetch price for {ticker}") from e
    
    async def get_index_prices(self, tickers: list) -> Dict[str, Price]:
        prices = {}
        for ticker in tickers:
            try:
                price = await self.get_index_price(ticker)
                prices[ticker] = price
            except Exception as e:
                logger.error(f"Failed to get price for {ticker}: {str(e)}")
                continue
        
        return prices
    
    async def test_connection(self) -> bool:
        try:
            async with self.http_client as client:
                response = await client.get("public/get_time")
                return "result" in response
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False