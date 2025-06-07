"""
Test module for FileReader and AdvancedFileReader classes.

This module contains comprehensive test cases for all functionality including
generators, decorators, magic methods, inheritance, and file operations.
"""

import pytest
import os
from file_reader import FileReader, AdvancedFileReader, color_decorator


def cleanup(*files):
    """Helper to clean up test files."""
    for f in files:
        if os.path.exists(f):
            os.remove(f)


def test_file_reader_basic():
    """Test FileReader initialization and basic functionality."""
    # Test empty init
    reader = FileReader()
    assert reader.filename is None
    
    # Test with file
    FileReader.create_sample_file("basic.txt", ["line1", "line2", "line3"])
    reader = FileReader("basic.txt")
    assert reader.filename == "basic.txt"
    assert len(reader._lines) == 3
    assert str(reader) == "FileReader('basic.txt', 3 lines)"
    cleanup("basic.txt")


def test_property_and_static_methods():
    """Test @property, @staticmethod, and @classmethod."""
    # Property test
    reader = FileReader()
    FileReader.create_sample_file("prop.txt", ["test"])
    reader.filename = "prop.txt"
    assert reader.filename == "prop.txt"
    
    # Static method test
    assert os.path.exists("prop.txt")
    with open("prop.txt", 'r') as f:
        assert f.read().strip() == "test"
    
    # Class method test
    reader2 = FileReader.from_content("class.txt", ["class", "method"])
    assert reader2.filename == "class.txt"
    assert reader2._lines == ["class", "method"]
    cleanup("prop.txt", "class.txt")


def test_generator_and_comprehension():
    """Test generator and list comprehension methods."""
    FileReader.create_sample_file("gen.txt", ["a", "b", "c"])
    reader = FileReader("gen.txt")
    
    # Generator test
    lines = list(reader.read_lines_generator())
    assert lines == ["a", "b", "c"]
    
    # List comprehension test
    lines2 = reader.get_lines_comprehension()
    assert lines2 == ["a", "b", "c"]
    cleanup("gen.txt")


def test_magic_methods():
    """Test __str__ and __add__ magic methods."""
    FileReader.create_sample_file("add1.txt", ["file1"])
    FileReader.create_sample_file("add2.txt", ["file2"])
    
    reader1 = FileReader("add1.txt")
    reader2 = FileReader("add2.txt")
    
    # Test __add__
    combined = reader1 + reader2
    assert len(combined._lines) == 2
    assert "file1" in combined._lines and "file2" in combined._lines
    
    # Test type error
    with pytest.raises(TypeError):
        reader1 + "not a FileReader"
    
    cleanup("add1.txt", "add2.txt", combined.filename)


def test_concatenate_methods():
    """Test file concatenation methods."""
    FileReader.create_sample_file("concat1.txt", ["a"])
    FileReader.create_sample_file("concat2.txt", ["b"])
    
    reader = FileReader("concat1.txt")
    result = reader.concatenate_files("concat2.txt")
    assert "Concatenated 2 files" in result
    cleanup("concat1.txt", "concat2.txt")


def test_advanced_reader():
    """Test AdvancedFileReader inheritance and features."""
    FileReader.create_sample_file("adv.txt", ["hello world", "python code"])
    reader = AdvancedFileReader("adv.txt")
    
    # Test inheritance
    assert isinstance(reader, FileReader)
    assert reader.stats['words'] == 4
    assert reader.stats['chars'] > 0
    
    # Test __str__ override
    result = str(reader)
    assert "3 words" in result
    
    # Test filtering
    FileReader.create_sample_file("filter.txt", ["python rocks", "java okay", "python great"])
    reader2 = AdvancedFileReader("filter.txt")
    filtered = reader2.filter_lines("python")
    assert len(filtered) == 2
    assert all("python" in line for line in filtered)
    
    cleanup("adv.txt", "filter.txt")


def test_color_decorator():
    """Test custom color decorator."""
    @color_decorator("red")
    def test_func():
        return "colored text"
    
    result = test_func()
    assert '\033[91m' in result  # Red color
    assert '\033[0m' in result   # Reset
    assert 'colored text' in result


def test_enhanced_concatenation():
    """Test AdvancedFileReader concatenation method."""
    FileReader.create_sample_file("multi1.txt", ["line1"])
    FileReader.create_sample_file("multi2.txt", ["line2"])
    FileReader.create_sample_file("multi3.txt", ["line3"])
    
    reader = AdvancedFileReader("multi1.txt")
    result = reader.concatenate_multiple_files(["multi2.txt", "multi3.txt"], "output.txt")
    
    assert "Created output.txt with 3 lines" in result
    assert os.path.exists("output.txt")
    cleanup("multi1.txt", "multi2.txt", "multi3.txt", "output.txt")


if __name__ == "__main__":
    pytest.main([__file__]) 