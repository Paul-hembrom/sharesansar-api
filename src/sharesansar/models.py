from dataclasses import dataclass
from typing import Optional, Dict, List
import pandas as pd

@dataclass
class StockInfo:
    symbol: str
    company: str
    ltp: float
    change: float
    change_percent: float
    open: float
    high: float
    low: float
    volume: int
    previous_close: float

@dataclass
class MarketSummary:
    total_traded_volume: int
    total_traded_amount: float
    total_transactions: int
    advances: int
    declines: int
    unchanged: int