"""Command-line interface for resqu"""

import argparse
import sys
from .api import api, getAPI


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Resqu - Fast API Response Fetcher")
    parser.add_argument("url", help="URL to fetch or file containing URLs")
    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument("-p", "--parallel", action="store_true", help="Use parallel fetching")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")
    
    args = parser.parse_args()
    
    if args.version:
        from . import __version__
        print(f"resqu version {__version__}")
        return
    
    if args.url.endswith('.txt'):
        results = getAPI(args.url, parallel=args.parallel)
        print(f"Fetched {len(results)} APIs")
    else:
        result = api(args.url, args.output)
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Successfully fetched {args.url}")
            print(f"Status: {result.get('status_code')}")
            print(f"Time: {result.get('response_time', 0):.3f}s")


if __name__ == "__main__":
    main()