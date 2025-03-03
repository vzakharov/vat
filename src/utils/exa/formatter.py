#!/usr/bin/env python3
#pyright: basic
"""
Formatting utilities for Exa search results.
"""
from typing import Optional
from ..common import FormatType, format_as_json, BaseFormatter
from .types import ExaResult

def format_single_result(results: ExaResult, output_format: FormatType) -> str:
    """Format a single search result in the specified format."""
    if output_format == "json":
        return format_as_json(results)
    
    query = results.get('query')
    if not query:
        return "ERROR: No query provided\n"
        
    formatted_text = f"Search results for: {query}\n\n"
    
    if "error" in results:
        return formatted_text + f"ERROR: {results['error']}\n"
    
    search_results = results.get("results", [])
    if not search_results:
        return formatted_text + "No results found.\n"
        
    for i, result in enumerate(search_results, 1):
        title = result.get('title', 'No title').strip()
        author = result.get('author', 'No author').strip()
        url = result.get('url', 'No URL').strip()
        
        formatted_text += f"{i}. {title}\n"
        formatted_text += f"   URL: {url}\n"
        formatted_text += f"   Snippet: {author}\n\n"
    
    return formatted_text

# Create formatter instance
formatter = BaseFormatter[ExaResult](
    single_format_func=format_single_result,
    single_label="QUERY",
    multi_label="MULTIPLE SEARCH RESULTS"
)

# Export the format_result function
format_result = formatter.format_result