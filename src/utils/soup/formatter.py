#!/usr/bin/env python3
"""
Formatting utilities for Soup text extraction results.
"""
from ..common import FormatType, format_as_json, BaseFormatter
from .types import SoupResult

def format_content_preview(content: str, max_length: int = 500, context_lines: int = 3) -> str:
    """Format content preview with smart truncation."""
    if len(content) <= max_length:
        return content
        
    lines = content.split('\n')
    if len(lines) <= context_lines * 2:
        return content[:max_length] + "..."
        
    start_lines = lines[:context_lines]
    end_lines = lines[-context_lines:]
    
    preview = "\n".join(start_lines)
    preview += "\n...\n[Content truncated]\n...\n"
    preview += "\n".join(end_lines)
    
    return preview

def format_single_output(data: SoupResult, output_format: FormatType) -> str:
    """Format a single extraction result in the specified format."""
    if output_format == "json":
        return format_as_json(data)
    
    url = data.get('url', 'Unknown URL')
    formatted_text = f"Extracted content from: {url}\n"
    
    if "error" in data:
        return formatted_text + f"ERROR: {data['error']}\n"
    
    formatted_text += f"Domain: {data.get('domain', 'Unknown')}\n"
    formatted_text += f"Title: {data.get('title', 'No title')}\n"
    formatted_text += f"Content length: {data.get('content_length', 0)} characters\n\n"
    
    content = data.get('content', '')
    if not content:
        formatted_text += "No content extracted\n"
        return formatted_text
    
    formatted_text += "CONTENT PREVIEW:\n"
    formatted_text += "=" * 80 + "\n"
    formatted_text += format_content_preview(content)
    formatted_text += "\n" + "=" * 80 + "\n"
    
    return formatted_text

# Create formatter instance
formatter = BaseFormatter[SoupResult](
    single_format_func=format_single_output,
    single_label="URL",
    multi_label="MULTIPLE URL EXTRACTION RESULTS"
)

# Export the format_result function
format_result = formatter.format_result