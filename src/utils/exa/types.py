#!/usr/bin/env python3
"""
Type definitions for Exa search functionality.
"""

from typing import List, TypedDict, Union
from ..common import BaseResult, ErrorResult

class ExaSearchResult(TypedDict):
    """Type for individual search result from Exa API"""
    title: str
    author: str
    url: str

class ExaApiResponse(BaseResult):
    """Type for successful Exa API response"""
    results: List[ExaSearchResult]

ExaResult = Union[ExaApiResponse, ErrorResult]