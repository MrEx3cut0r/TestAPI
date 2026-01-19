from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, BigInteger, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PriceModel(Base):    
    __tablename__ = "prices"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(20), nullable=False, index=True)
    price = Column(Float, nullable=False)
    timestamp = Column(BigInteger, nullable=False, index=True)
    
    __table_args__ = (
        Index('ix_ticker_timestamp', 'ticker', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<PriceModel(ticker={self.ticker}, price={self.price}, timestamp={self.timestamp})>"
    
    @classmethod
    def from_domain(cls, price):
        return cls(
            id=price.id,
            ticker=price.ticker,
            price=price.price,
            timestamp=price.timestamp
        )
    
    def to_domain(self):
        from src.domain.entities.price import Price
        return Price(
            id=self.id,
            ticker=self.ticker,
            price=self.price,
            timestamp=self.timestamp
        )