from dataclasses import dataclass
from enum import Enum


class CurrencyPair(str, Enum):
    BTC_USD = "btc_usd"
    ETH_USD = "eth_usd"
    
    @classmethod
    def list(cls):
        return [pair.value for pair in cls]
    
    @classmethod
    def get_base_currency(cls, pair: str) -> str:
        return pair.split('_')[0].upper()


@dataclass(frozen=True)
class Ticker:    
    value: str
    
    def __post_init__(self):
        if self.value not in CurrencyPair.list():
            raise ValueError(f"Invalid ticker. Supported tickers: {CurrencyPair.list()}")
    
    @property
    def base_currency(self) -> str:
        return CurrencyPair.get_base_currency(self.value)