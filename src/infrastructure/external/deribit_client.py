import aiohttp
import logging
from typing import Dict
from datetime import datetime
from src.domain.ports.market_data_provider import MarketDataProvider
from src.domain.entities.price import Price
from .aiohttp_client import AioHttpClient

logger = logging.getLogger(__name__)


class DeribitClient(MarketDataProvider):    
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.http_client = AioHttpClient(base_url=api_url)
        
        self.index_mapping = {
            "btc_usd": "btc_usd",  
            "eth_usd": "eth_usd",
        }
    
    async def get_index_price(self, ticker: str) -> Price:
        valid_index_map = {
            "btc_usd": "btc_usd",   
            "eth_usd": "eth_usd",  
        }

        index_name = valid_index_map.get(ticker)
        
        if not index_name:
            raise ValueError(
                f"Unsupported ticker for index price: '{ticker}'. "
                f"Supported tickers: {list(valid_index_map.keys())}"
            )

        try:
            async with self.http_client as client:
                response = await client.get(
                    "public/get_index_price",
                    params={"index_name": index_name}
                )
                
                result = response.get("result", {})
                price_value = result.get("index_price")

                if price_value is None:
                    price_value = result.get("estimated_delivery_price")
                
                price = float(price_value) if price_value else 0.0
                timestamp = int(datetime.now().timestamp())

                if price <= 0:
                    raise ValueError(f"Invalid or zero price received for {ticker}: {price}")

                return Price(
                    ticker=ticker,
                    price=price,
                    timestamp=timestamp
                )
                    
        except Exception as e:
                raise 
        
        logger.error(f"All index formats failed for {ticker}")
        raise RuntimeError(f"Failed to fetch price for {ticker}. Last error: {last_error}")
    
    async def get_index_prices(self, tickers: list) -> Dict[str, Price]:
        prices = {}
        
        for ticker in tickers:
            try:
                price = await self.get_index_price(ticker)
                prices[ticker] = price
                logger.info(f"Successfully fetched price for {ticker}: {price.price}")
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