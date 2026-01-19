from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class UnixTimestamp:
    
    value: int
    
    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Timestamp must be positive")
    
    @classmethod
    def now(cls) -> 'UnixTimestamp':
        return cls(int(datetime.now().timestamp()))
    
    @classmethod
    def from_datetime(cls, dt: datetime) -> 'UnixTimestamp':
        return cls(int(dt.timestamp()))
    
    def to_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.value)