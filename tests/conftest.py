"""Pytest configuration and fixtures."""

import pytest
import logging


# Configure logging for tests
logging.basicConfig(level=logging.INFO)


@pytest.fixture
def temp_dir(tmp_path):
    """Provide a temporary directory for test files."""
    return tmp_path
