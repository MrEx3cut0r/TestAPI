from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Price:    
    id: Optional[int] = None
    ticker: str = ""
    price: float = 0.0
    timestamp: int = 0
    
    def __post_init__(self):
        if not self.ticker:
            raise ValueError("Ticker cannot be empty")
        if self.price <= 0:
            raise ValueError("Price must be positive")
        if self.timestamp <= 0:
            raise ValueError("Timestamp must be positive")
    
    @property
    def datetime(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp)
    
    def is_recent(self, minutes: int = 5) -> bool:
        current_time = int(datetime.now().timestamp())
        return (current_time - self.timestamp) <= (minutes * 60)