#!/usr/bin/env python3
"""
Formatting utilities for Exa search results.
"""
from typing import Optional
from ..common import FormatType, format_as_json, BaseFormatter
from .types import ExaResult

def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """Truncate text to max_length, ensuring we don't cut words in half."""
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length]
    last_space = truncated.rfind(" ")
    if last_space > 0:
        truncated = truncated[:last_space]
    return truncated + suffix

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
        url = result.get('url', 'No URL').strip()
        snippet = result.get('snippet', 'No snippet').strip()
        
        formatted_text += f"{i}. {title}\n"
        formatted_text += f"   URL: {url}\n"
        formatted_text += f"   Snippet: {truncate_text(snippet)}\n\n"
    
    return formatted_text

# Create formatter instance
formatter = BaseFormatter[ExaResult](
    single_format_func=format_single_result,
    single_label="QUERY",
    multi_label="MULTIPLE SEARCH RESULTS"
)

# Export the format_result function
format_result = formatter.format_result