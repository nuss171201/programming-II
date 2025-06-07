# File Reader Project

.PHONY: help install test clean

help:
	@echo "Available commands:"
	@echo "  install - Install dependencies"
	@echo "  test    - Run tests"
	@echo "  clean   - Clean up files"

install:
	pip install -r requirements.txt

test:
	pytest test_file_reader.py -v

clean:
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -name "*.txt" -not -name "requirements.txt" -delete
	find . -name "*.pyc" -delete 