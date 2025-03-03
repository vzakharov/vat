#!/usr/bin/env python3
"""
Exa Search Tool
A command-line utility that searches the web using the Exa API.
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Import shared utilities
from src.utils.exa.types import ExaApiResponse, ExaResult, ExaSearchResult
from src.utils.exa.formatter import format_result
from src.utils.common import ErrorResult
from src.utils.cli.base import ToolRunner

# Load environment variables
load_dotenv()

EXA_API_KEY = os.getenv("EXA_API_KEY")
DEFAULT_SEARCH_LIMIT = int(os.getenv("DEFAULT_SEARCH_LIMIT", "10"))
EXA_API_URL = "https://api.exa.ai/search"

def search_exa(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> ExaResult:
    """
    Perform a web search using the Exa API.
    
    Args:
        query: The search query string
        limit: Maximum number of results to return
        
    Returns:
        Dictionary containing search results or error information
    """
    # Validate environment and inputs
    if not query or query.isspace():
        return ErrorResult(query=query, error="Empty query provided")
    
    if not EXA_API_KEY:
        return ErrorResult(query=query, error="EXA_API_KEY not found in environment variables")
    
    if limit < 1:
        limit = DEFAULT_SEARCH_LIMIT
    
    headers = {
        "Authorization": f"Bearer {EXA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": query,
        "numResults": limit,
        "useAutoprompt": True
    }
    
    try:
        response = requests.post(EXA_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if not isinstance(result, dict) or 'results' not in result:
            return ErrorResult(query=query, error="Invalid API response format")
        
        return ExaApiResponse(
            query=query, 
            results=[
                ExaSearchResult(
                    title=item.get('title', 'No title'),
                    url=item.get('url', 'No URL'),
                    snippet=item.get('text', 'No snippet')
                ) 
                for item in result.get('results', [])
            ]
        )
    except requests.exceptions.Timeout:
        return ErrorResult(query=query, error="Request timed out")
    except requests.exceptions.RequestException as e:
        return ErrorResult(query=query, error=str(e))
    except (KeyError, ValueError, TypeError) as e:
        return ErrorResult(query=query, error=f"Error processing API response: {str(e)}")

def main():
    runner = ToolRunner(
        processor=search_exa,
        formatter=format_result,
        description="Search the web using Exa API",
        input_name="query",
        input_help="Single search query",
        multi_input_help="Multiple search queries"
    )
    
    runner.add_arguments(limit={
        "type": int,
        "default": DEFAULT_SEARCH_LIMIT,
        "help": f"Number of results (default: {DEFAULT_SEARCH_LIMIT})"
    })
    
    runner.run()

if __name__ == "__main__":
    main()
