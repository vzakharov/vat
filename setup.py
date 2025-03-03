#!/usr/bin/env python3
"""
VAT package setup
"""

from setuptools import setup, find_packages

setup(
    name="vat",
    version="0.1.0",
    description="VSCode Agent Toolbox package",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "beautifulsoup4",
        "requests",
        "python-dotenv",
        "inflect",
    ],
)