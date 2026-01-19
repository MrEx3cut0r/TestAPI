import aiohttp
import asyncio
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class AioHttpClient:    
    def __init__(self, base_url: str = None, timeout: int = 10):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        if not self.session:
            raise RuntimeError("Session not initialized. Use async with context.")
        
        url = f"{self.base_url}/{endpoint}" if self.base_url else endpoint
        
        try:
            async with self.session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"HTTP request failed: {str(e)}")
            raise
    
    async def post(self, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        if not self.session:
            raise RuntimeError("Session not initialized. Use async with context.")
        
        url = f"{self.base_url}/{endpoint}" if self.base_url else endpoint
        
        try:
            async with self.session.post(url, json=data) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"HTTP request failed: {str(e)}")
            raise