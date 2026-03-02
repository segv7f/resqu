import asyncio
import aiohttp
from typing import List, Dict, Any, Union
from pathlib import Path
import time
from datetime import datetime

class FastAPIFetcher:
    """High-performance concurrent API fetcher"""
    
    def __init__(self, max_concurrent: int = 100, timeout: int = 10):
        """
        Initialize fast fetcher
        
        Args:
            max_concurrent: Maximum concurrent connections
            timeout: Request timeout in seconds
        """
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self.results = []
        
    async def _fetch_single(self, session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        """Fetch a single API asynchronously"""
        start_time = time.time()
        
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = f'http://{url}'
                
            async with session.get(url, timeout=self.timeout) as response:
                content = await response.text()
                
                return {
                    'url': url,
                    'status_code': response.status,
                    'headers': dict(response.headers),
                    'content': content[:5000],  # Limit content to 5000 chars
                    'success': True,
                    'response_time': time.time() - start_time,
                    'timestamp': datetime.now().isoformat()
                }
                
        except asyncio.TimeoutError:
            return {
                'url': url,
                'error': 'Timeout',
                'success': False,
                'response_time': time.time() - start_time
            }
        except Exception as e:
            return {
                'url': url,
                'error': str(e),
                'success': False,
                'response_time': time.time() - start_time
            }
    
    async def fetch_many(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Fetch multiple APIs concurrently"""
        connector = aiohttp.TCPConnector(limit=self.max_concurrent)
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            tasks = [self._fetch_single(session, url) for url in urls]
            self.results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter out exceptions
            self.results = [
                r if not isinstance(r, Exception) else {'url': 'unknown', 'error': str(r), 'success': False}
                for r in self.results
            ]
            
            return self.results
    
    def fetch_many_sync(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Synchronous wrapper for fetch_many"""
        return asyncio.run(self.fetch_many(urls))


def parse_urls_from_file(filename: str) -> List[str]:
    """Read URLs from file"""
    path = Path(filename)
    if not path.exists():
        return []
    
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


def save_results(results: List[Dict[str, Any]], output_dir: str = "requsAPItxt") -> None:
    """Save multiple results to files"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for result in results:
        if result.get('success', False):
            clean_url = result['url'].replace('http://', '').replace('https://', '').replace('/', '_')
            filename = output_path / f"{clean_url}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"URL: {result['url']}\n")
                f.write(f"Status Code: {result.get('status_code', 'N/A')}\n")
                f.write(f"Response Time: {result.get('response_time', 0):.3f}s\n")
                f.write(f"Timestamp: {result.get('timestamp', datetime.now().isoformat())}\n")
                
                f.write(f"\n--- Headers ---\n")
                for key, value in result.get('headers', {}).items():
                    f.write(f"{key}: {value}\n")
                
                f.write(f"\n--- Response Content ---\n")
                f.write(result.get('content', ''))