import asyncio
import aiohttp
import requests
from pathlib import Path
from datetime import datetime
import time
from typing import Union, List, Optional

class API:
    """Main API class for fetching and saving responses"""
    
    def __init__(self, url: str, output_file: Optional[str] = None):
        """
        Initialize API fetcher
        
        Args:
            url: URL to fetch
            output_file: Optional output file name
        """
        self.url = url if url.startswith(('http://', 'https://')) else f'http://{url}'
        self.output_file = output_file
        self.responses = []
        
    def _save_response(self, data: dict) -> None:
        """Save response to file"""
        # Clean filename
        clean_url = data['url'].replace('http://', '').replace('https://', '').replace('/', '_')
        filename = f"{clean_url}.txt"
        
        # Create directory if not exists
        output_dir = Path("requsAPItxt")
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"URL: {data['url']}\n")
            f.write(f"Method: {data.get('method', 'GET')}\n")
            f.write(f"Status Code: {data.get('status_code', 200)}\n")
            f.write(f"Time: {data.get('timestamp', datetime.now().isoformat())}\n")
            f.write(f"Response Time: {data.get('response_time', 0):.3f}s\n")
            
            f.write(f"\n--- Headers ---\n")
            for key, value in data.get('headers', {}).items():
                f.write(f"{key}: {value}\n")
            
            f.write(f"\n--- Response Content ---\n")
            f.write(data.get('content', ''))
            
            f.write(f"\n\n--- Curl Command ---\n")
            f.write(self._generate_curl(data))
            
    def _generate_curl(self, data: dict) -> str:
        """Generate curl command from response"""
        curl = f"curl -X {data.get('method', 'GET')} '{data['url']}'"
        if data.get('headers'):
            for key, value in data['headers'].items():
                curl += f" -H '{key}: {value}'"
        return curl
        
    def fetch_sync(self) -> dict:
        """Synchronous fetch"""
        try:
            start_time = time.time()
            response = requests.get(self.url, timeout=10)
            
            data = {
                'url': self.url,
                'method': 'GET',
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content': response.text,
                'timestamp': datetime.now().isoformat(),
                'response_time': time.time() - start_time
            }
            
            self.responses.append(data)
            self._save_response(data)
            return data
            
        except Exception as e:
            error_data = {
                'url': self.url,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            return error_data
    
    async def fetch_async(self) -> dict:
        """Asynchronous fetch"""
        try:
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, timeout=10) as response:
                    content = await response.text()
                    
                    data = {
                        'url': self.url,
                        'method': 'GET',
                        'status_code': response.status,
                        'headers': dict(response.headers),
                        'content': content,
                        'timestamp': datetime.now().isoformat(),
                        'response_time': time.time() - start_time
                    }
                    
                    self.responses.append(data)
                    self._save_response(data)
                    return data
                    
        except Exception as e:
            error_data = {
                'url': self.url,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            return error_data
    
    def get(self, async_mode: bool = True) -> dict:
        """Get response from API"""
        if async_mode:
            return asyncio.run(self.fetch_async())
        else:
            return self.fetch_sync()


def api(url: str, textfile: Optional[str] = None) -> dict:
    """
    Main function to call API and save results
    
    Args:
        url: URL to fetch
        textfile: Output file name (if None, auto-generated)
    
    Returns:
        dict: Response data
    """
    api_instance = API(url, textfile)
    return api_instance.get()


def getAPI(url: Union[str, List[str]], parallel: bool = True) -> Union[dict, List[dict]]:
    """
    Fast API fetcher utility
    
    Args:
        url: URL string, list of URLs, or path to file containing URLs
        parallel: Whether to fetch in parallel (faster)
    
    Returns:
        Single response dict or list of response dicts
    """
    from .utils import FastAPIFetcher
    
    fetcher = FastAPIFetcher()
    
    if isinstance(url, str):
        # Check if it's a file path
        if url.endswith('.txt'):
            from .utils import parse_urls_from_file
            urls = parse_urls_from_file(url)
            if parallel:
                return fetcher.fetch_many(urls)
            else:
                return [requests.get(u).text for u in urls]
        else:
            # Single URL
            api_instance = API(url)
            return api_instance.get()
            
    elif isinstance(url, list):
        # List of URLs
        if parallel:
            return fetcher.fetch_many(url)
        else:
            return [API(u).get() for u in url]