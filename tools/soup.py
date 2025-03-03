#!/usr/bin/env python3
"""
Soup Text Extraction Tool
A command-line utility that extracts meaningful text from webpages using BeautifulSoup.
"""
import os
import sys
import requests
from typing import Optional, List
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from src.utils.soup.types import SoupResult, SoupExtractedContent
from src.utils.soup.formatter import format_result
from src.utils.common import ErrorResult
from src.utils.cli.base import ToolRunner

def clean_text(text: str) -> str:
    """Clean extracted text by removing extra whitespace and empty lines."""
    lines = [line.strip() for line in text.split("\n")]
    return "\n".join(line for line in lines if line)

def get_main_content_elements() -> List[dict]:
    """Get list of potential main content element selectors."""
    return [
        {"tag": "main"},
        {"tag": "article"},
        {"tag": "div", "attrs": {"id": "content"}},
        {"tag": "div", "attrs": {"class": "content"}},
        {"tag": "div", "attrs": {"id": "main"}},
        {"tag": "div", "attrs": {"class": "main"}},
        {"tag": "div", "attrs": {"role": "main"}},
    ]

def extract_text_from_url(url: str, selector: Optional[str] = None) -> SoupResult:
    """
    Extract text content from a webpage.
    
    Args:
        url: The URL to scrape
        selector: Optional CSS selector to target specific elements
        
    Returns:
        Dictionary containing the extracted content
    """
    if not url or url.isspace():
        return ErrorResult(query=url, error="Empty URL provided")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(["script", "style", "meta", "noscript", "header", "footer", "nav"]):
            element.decompose()
            
        # Extract title and content
        title = soup.title.string.strip() if soup.title else urlparse(url).path
        content = extract_content(soup, selector)
        
        # Clean up the text
        content = clean_text(content)
        domain = urlparse(url).netloc
        
        return SoupExtractedContent(
            query=url,
            url=url,
            domain=domain,
            title=title,
            content=content,
            content_length=len(content)
        )
        
    except requests.exceptions.Timeout:
        return ErrorResult(query=url, error="Request timed out")
    except requests.exceptions.RequestException as e:
        return ErrorResult(query=url, error=str(e))
    except Exception as e:
        return ErrorResult(query=url, error=f"Error processing content: {str(e)}")

def extract_content(soup: BeautifulSoup, selector: Optional[str] = None) -> str:
    """Extract content from BeautifulSoup object using selector or fallback methods."""
    if selector:
        elements = soup.select(selector)
        if elements:
            return "\n\n".join(elem.get_text(separator="\n", strip=True) for elem in elements)
    
    # Try each potential main content element
    for element_def in get_main_content_elements():
        element = soup.find(element_def["tag"], element_def.get("attrs"))
        if element:
            content = element.get_text(separator="\n", strip=True)
            if len(content) > 100:  # Only use if substantial content found
                return content
    
    # Fallback to body text
    if soup.body:
        return soup.body.get_text(separator="\n", strip=True)
    
    return "No content found"

def main():
    runner = ToolRunner(
        processor=extract_text_from_url,
        formatter=format_result,
        description="Extract text from webpages using BeautifulSoup",
        input_name="url",
        input_help="URL to extract text from",
        multi_input_help="Multiple URLs to extract text from"
    )
    
    runner.add_arguments(selector={
        "type": str,
        "help": "CSS selector to target specific elements"
    })
    
    runner.run()

if __name__ == "__main__":
    main()