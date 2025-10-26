import requests
import pandas as pd
from typing import Dict, Any, Optional
import time
from datetime import datetime

def safe_float_conversion(value, default=0.0):
    """Safely convert value to float."""
    try:
        if pd.isna(value) or value == '' or value == '-':
            return default
        if isinstance(value, str):
            value = value.replace(',', '').replace('%', '')
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int_conversion(value, default=0):
    """Safely convert value to int."""
    try:
        if pd.isna(value) or value == '' or value == '-':
            return default
        if isinstance(value, str):
            value = value.replace(',', '')
        return int(float(value))
    except (ValueError, TypeError):
        return default

def validate_date(date_string: str) -> bool:
    """Validate date string format YYYY-MM-DD."""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def format_date(date_obj) -> str:
    """Format datetime object to YYYY-MM-DD."""
    return date_obj.strftime('%Y-%m-%d')