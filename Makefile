.PHONY: help install format lint type-check test clean

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies using uv"
	@echo "  format       - Format code using isort"
	@echo "  lint         - Run isort in check mode"
	@echo "  type-check   - Run mypy type checking"
	@echo "  check        - Run both lint and type-check"
	@echo "  test         - Run tests using tox"
	@echo "  clean        - Clean up cache files"

# Install dependencies
install:
	uv sync

# Format code with isort
format:
	uv run isort .

# Check code formatting with isort
lint:
	uv run isort --check-only --diff .

# Run type checking with mypy
type-check:
	uv run mypy .

# Run both lint and type-check
check: lint type-check

# Run tests
test:
	uv run tox

# Clean up cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
