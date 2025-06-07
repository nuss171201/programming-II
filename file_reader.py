"""
File Reader Module

This module provides classes for reading and manipulating files with generators,
decorators, and object-oriented programming concepts.
"""

import os
from typing import Generator, List, Optional


def color_decorator(color: str):
    """Simple color decorator using ANSI codes."""
    colors = {'red': '\033[91m', 'green': '\033[92m', 'blue': '\033[94m', 'reset': '\033[0m'}
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"{colors.get(color, colors['red'])}{result}{colors['reset']}"
        return wrapper
    return decorator


class FileReader:
    """Custom object type for reading files using generators."""
    
    def __init__(self, filename: str = None):
        self._filename = filename
        self._lines = []
        if filename and os.path.exists(filename):
            self._load_file()
    
    @property
    def filename(self):
        return self._filename
    
    @filename.setter
    def filename(self, value):
        self._filename = value
        if value and os.path.exists(value):
            self._load_file()
    
    def _load_file(self):
        with open(self._filename, 'r') as file:
            self._lines = [line.strip() for line in file]
    
    def read_lines_generator(self) -> Generator[str, None, None]:
        """Generator that yields lines from file."""
        if self._filename and os.path.exists(self._filename):
            with open(self._filename, 'r') as file:
                for line in file:
                    yield line.strip()
    
    def get_lines_comprehension(self) -> List[str]:
        """Get lines using list comprehension."""
        return [line.strip() for line in open(self._filename, 'r')] if self._filename else []
    
    @staticmethod
    def create_sample_file(filename: str, content: List[str]):
        """Static method to create a file."""
        with open(filename, 'w') as f:
            f.write('\n'.join(content))
    
    @classmethod
    def from_content(cls, filename: str, content: List[str]):
        """Class method to create FileReader with content."""
        cls.create_sample_file(filename, content)
        return cls(filename)
    
    def __str__(self):
        return f"FileReader('{self._filename}', {len(self._lines)} lines)"
    
    def __add__(self, other):
        """Concatenate two FileReader objects."""
        if not isinstance(other, FileReader):
            raise TypeError("Can only add FileReader instances")
        
        combined_lines = self._lines + other._lines
        new_filename = f"combined_{os.path.basename(self._filename or 'file1')}_{os.path.basename(other._filename or 'file2')}.txt"
        return FileReader.from_content(new_filename, combined_lines)
    
    @color_decorator("green")
    def concatenate_files(self, *filenames):
        """Method to concatenate multiple files."""
        result = self
        for filename in filenames:
            if os.path.exists(filename):
                other = FileReader(filename)
                result = result + other
        return f"Concatenated {len(filenames) + 1} files"


class AdvancedFileReader(FileReader):
    """Child class with extra functionality."""
    
    def __init__(self, filename: str = None):
        super().__init__(filename)
        self._stats = self._calculate_stats()
    
    def _calculate_stats(self):
        """Calculate file statistics."""
        if not self._lines:
            return {'words': 0, 'chars': 0}
        
        words = sum(len(line.split()) for line in self._lines)
        chars = sum(len(line) for line in self._lines)
        return {'words': words, 'chars': chars}
    
    @property
    def stats(self):
        return self._stats
    
    def filter_lines(self, keyword: str) -> List[str]:
        """Filter lines containing keyword using list comprehension."""
        return [line for line in self._lines if keyword.lower() in line.lower()]
    
    @color_decorator("blue")
    def __str__(self):
        base = super().__str__()
        return base.replace(')', f', {self._stats["words"]} words)')
    
    def concatenate_multiple_files(self, filenames: List[str], output: str = "output.txt"):
        """Enhanced concatenation method."""
        all_lines = self._lines.copy()
        for filename in filenames:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    all_lines.extend(line.strip() for line in f)
        
        with open(output, 'w') as f:
            f.write('\n'.join(all_lines))
        
        return f"Created {output} with {len(all_lines)} lines" 