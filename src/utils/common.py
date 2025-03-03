#!/usr/bin/env python3
"""
Common utilities and base types for web tools.
"""

import os
import json
from typing import Any, TypedDict, Literal, Union, List, TypeVar, Generic, Callable

# Base types
class BaseResult(TypedDict):
    """Base type for all results"""
    query: str  # For search results or URL for soup results

class ErrorResult(BaseResult):
    """Type for error results"""
    error: str

# Format types
# FormatType = Literal["text", "json"]
FormatType = str

# Generic type for results
T = TypeVar('T', bound=Union[BaseResult, ErrorResult])

class BaseFormatter(Generic[T]):
    """Base formatter for tool results."""
    
    def __init__(self, 
                 single_format_func: Callable[[T, FormatType], str],
                 single_label: str = "RESULT",
                 multi_label: str = "MULTIPLE RESULTS"):
        self.single_format_func = single_format_func
        self.single_label = single_label
        self.multi_label = multi_label
    
    def format_result(self, data: Union[T, List[T]], output_format: FormatType) -> str:
        """Format results in the specified format."""
        if isinstance(data, list):
            return self.format_multiple_results(data, output_format)
        return self.single_format_func(data, output_format)
    
    def format_multiple_results(self, all_data: List[T], output_format: FormatType) -> str:
        """Format multiple results in the specified format."""
        if output_format == "json":
            return format_as_json(all_data)
        
        formatted_text = f"{self.multi_label}\n\n"
        
        for idx, data in enumerate(all_data, 1):
            formatted_text += f"===== {self.single_label} {idx}: {data.get('query', 'Unknown')} =====\n"
            formatted_text += self.single_format_func(data, "text")  # Always use text format for nested results
            formatted_text += "\n"
        
        return formatted_text

def save_to_file(content: str, filename: str) -> None:
    """
    Save content to a file in the output directory.
    
    Args:
        content: The content to save
        filename: Name of the output file
    """
    # Get the project root directory (3 levels up from this file)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    filepath = os.path.join(project_root, filename)
    
    # Create directories if they don't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Results saved to {filepath}")

def format_as_json(data: Any) -> str:
    """
    Format data as pretty-printed JSON.
    
    Args:
        data: Data to format as JSON
    
    Returns:
        JSON formatted string
    """
    return json.dumps(data, indent=2, ensure_ascii=False)