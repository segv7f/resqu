"""Resqu - Fast API Response Fetcher

A high-performance tool for fetching and saving API responses.
"""

from .api import API, api, getAPI
from .utils import FastAPIFetcher

__version__ = "1.0.0"
__all__ = ['API', 'api', 'getAPI', 'FastAPIFetcher']

# Tiện ích để gọi nhanh
getAPI_text = api