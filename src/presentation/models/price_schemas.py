from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List



class PriceBase(BaseModel):
    ticker: str = Field(..., min_length=3, max_length=20)
    value: float = Field(..., gt=0) 
    timestamp: int = Field(..., gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "ticker": "btc_usd",
                "value": 45000.50,
                "timestamp": 1700000000
            }
        }

class PriceResponse(PriceBase):
    id: int
    datetime: datetime = Field(..., description="Дата и время в читаемом формате")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "ticker": "btc_usd",
                "value": 45000.50,
                "timestamp": 1700000000,
                "datetime": "2023-11-15T00:00:00"
            }
        }
class PriceCreate(PriceBase):
    pass


class PriceListResponse(BaseModel):
    ticker: str
    prices: List[PriceResponse]
    count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "ticker": "btc_usd",
                "prices": [
                    {
                        "id": 1,
                        "ticker": "btc_usd",
                        "price": 45000.50,
                        "timestamp": 1700000000,
                        "datetime": "2023-11-15T00:00:00"
                    }
                ],
                "count": 1
            }
        }


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Price not found",
                "error_code": "PRICE_NOT_FOUND"
            }
        }


PriceBase.Config.json_schema_extra = {
    "example": {
        "ticker": "btc_usd",
        "price": 45000.50,
        "timestamp": 1700000000
    }
}