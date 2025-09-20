"""
Simple tests for CI/CD pipeline
"""

import pytest


def test_basic():
    """Basic test to ensure CI/CD is functioning"""
    assert True


def test_math():
    """Simple arithmetic test"""
    assert 2 + 2 == 4
    assert 10 * 5 == 50
    assert 100 / 4 == 25.0


def test_imports():
    """Test that key modules can be imported"""
    try:
        import fastapi
        import sqlalchemy
        import alembic
        import pydantic
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import required modules: {e}")


def test_environment():
    """Test environment setup"""
    import sys
    assert sys.version_info.major >= 3
    assert sys.version_info.minor >= 8


def test_string_operations():
    """Test string operations"""
    test_str = "Hello World"
    assert test_str.lower() == "hello world"
    assert test_str.upper() == "HELLO WORLD"
    assert len(test_str) == 11


def test_list_operations():
    """Test list operations"""
    test_list = [1, 2, 3, 4, 5]
    assert len(test_list) == 5
    assert sum(test_list) == 15
    assert max(test_list) == 5
    assert min(test_list) == 1
