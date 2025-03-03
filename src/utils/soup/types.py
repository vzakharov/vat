#!/usr/bin/env python3
"""
Type definitions for Soup text extraction functionality.
"""

from typing import Union, TypedDict
from ..common import BaseResult, ErrorResult

class SoupExtractedContent(BaseResult):
    """Type for content extracted by BeautifulSoup"""
    url: str
    domain: str
    title: str
    content: str
    content_length: int

SoupResult = Union[SoupExtractedContent, ErrorResult]