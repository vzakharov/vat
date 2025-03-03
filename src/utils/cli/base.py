#!/usr/bin/env python3
"""
Common CLI utilities and base classes.
"""

import os
import sys
import inflect
import argparse
import concurrent.futures
from typing import TypeVar, Generic, List, Callable, Optional, Union, Dict, Any
from dotenv import load_dotenv

# Load environment variables once
load_dotenv()
MAX_PARALLEL_REQUESTS = int(os.getenv("MAX_PARALLEL_REQUESTS", "5"))

# Initialize the inflect engine
p = inflect.engine()

T = TypeVar('T')

class ParallelProcessor(Generic[T]):
    """Base class for parallel processing of items."""
    
    def __init__(self, processor: Callable[..., T], max_items: int = MAX_PARALLEL_REQUESTS):
        self.processor = processor
        self.max_items = max_items
    
    def process_items(self, items: List[str], **kwargs) -> List[T]:
        """Process multiple items in parallel."""
        if len(items) > self.max_items:
            print(f"Warning: Maximum {self.max_items} parallel requests allowed. Only the first {self.max_items} will be processed.")
            items = items[:self.max_items]
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.processor, item, **kwargs) 
                for item in items
            ]
            return [future.result() for future in concurrent.futures.as_completed(futures)]

def create_output_parser(description: str, 
                        input_name: str,
                        input_help: str,
                        multi_input_help: Optional[str] = None) -> argparse.ArgumentParser:
    """Create a standard parser for tools with common arguments."""
    parser = argparse.ArgumentParser(description=description)
    
    # Create mutually exclusive group for single/multiple inputs
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(f"--{input_name}", f"-{input_name[0]}", 
                           type=str, help=input_help)
    
    if multi_input_help:
        plural_name = p.plural(input_name)
        input_group.add_argument(f"--{plural_name}", f"-{input_name[0]}s", 
                               nargs="+", type=str,
                               help=f"{multi_input_help} (up to {MAX_PARALLEL_REQUESTS})")
    
    # Common arguments
    parser.add_argument("--format", "-f", 
                       choices=["text", "json"], 
                       default="text",
                       help="Output format (default: text)")
    parser.add_argument("--output", "-o", 
                       type=str,
                       help="Save results to file (in output directory)")
    
    return parser

class ToolRunner(Generic[T]):
    """Base class for running tools with standard CLI patterns."""
    
    def __init__(self,
                 processor: Callable[..., T],
                 formatter: Callable[[Union[T, List[T]], str], str],
                 description: str,
                 input_name: str,
                 input_help: str,
                 multi_input_help: Optional[str] = None):
        self.processor = processor
        self.formatter = formatter
        self.input_name = input_name
        self.plural_name = p.plural(input_name)
        self.parser = create_output_parser(
            description=description,
            input_name=input_name,
            input_help=input_help,
            multi_input_help=multi_input_help
        )
        self.parallel_processor = ParallelProcessor(processor)
    
    def add_arguments(self, **kwargs: Dict[str, Any]) -> None:
        """Add additional tool-specific arguments to the parser."""
        for name, options in kwargs.items():
            self.parser.add_argument(f"--{name}", f"-{name[0]}", **options)
    
    def run(self) -> None:
        """Run the tool with parsed arguments."""
        args = self.parser.parse_args()
        
        # Get the input value and any additional args
        input_args = {k: v for k, v in vars(args).items() 
                     if k not in ['format', 'output']}
        
        # Process single or multiple inputs using proper plural form
        single_input = input_args.get(self.input_name)
        multi_inputs = input_args.get(self.plural_name)
        
        # Remove the inputs from kwargs
        kwargs = {k: v for k, v in input_args.items() 
                 if v is not None and k not in [self.input_name, self.plural_name]}
        
        try:
            if single_input:
                results = self.processor(single_input, **kwargs)
            else:
                results = self.parallel_processor.process_items(multi_inputs, **kwargs)
            
            # Format and output results
            formatted_results = self.formatter(results, args.format)
            
            if args.output:
                from ..common import save_to_file
                try:
                    save_to_file(formatted_results, args.output)
                except Exception as e:
                    print(f"Error saving results: {str(e)}", file=sys.stderr)
                    sys.exit(1)
            else:
                print(formatted_results)
        except Exception as e:
            print(f"Error processing request: {str(e)}", file=sys.stderr)
            sys.exit(1)