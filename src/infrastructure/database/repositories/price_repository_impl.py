from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_
from src.domain.ports.price_repository import PriceRepository
from src.domain.entities.price import Price
from src.infrastructure.database.models.price_model import PriceModel


class PriceRepositoryImpl(PriceRepository):
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, price: Price) -> Price:
        price_model = PriceModel.from_domain(price)
        
        if price.id:
            existing = await self.session.get(PriceModel, price.id)
            if existing:
                existing.price = price.price
                existing.timestamp = price.timestamp
                price_model = existing
        
        self.session.add(price_model)
        await self.session.flush([price_model])
        await self.session.refresh(price_model)
        
        return price_model.to_domain()
    
    async def get_all(self, ticker: str) -> List[Price]:
        stmt = select(PriceModel).where(
            PriceModel.ticker == ticker
        ).order_by(PriceModel.timestamp.desc())
        
        result = await self.session.execute(stmt)
        price_models = result.scalars().all()
        
        return [price_model.to_domain() for price_model in price_models]
    
    async def get_last(self, ticker: str) -> Optional[Price]:
        stmt = select(PriceModel).where(
            PriceModel.ticker == ticker
        ).order_by(desc(PriceModel.timestamp)).limit(1)
        
        result = await self.session.execute(stmt)
        price_model = result.scalar_one_or_none()
        
        if price_model:
            return price_model.to_domain()
        return None
    
    async def get_by_date_range(
        self, 
        ticker: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Price]:
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())
        
        stmt = select(PriceModel).where(
            and_(
                PriceModel.ticker == ticker,
                PriceModel.timestamp >= start_timestamp,
                PriceModel.timestamp <= end_timestamp
            )
        ).order_by(PriceModel.timestamp.desc())
        
        result = await self.session.execute(stmt)
        price_models = result.scalars().all()
        
        return [price_model.to_domain() for price_model in price_models]
    
    async def batch_save(self, prices: List[Price]) -> List[Price]:
        saved_prices = []
        
        price_models = [PriceModel.from_domain(price) for price in prices]
        self.session.add_all(price_models)
        
        return [price_model.to_domain() for price_model in price_models]