"""Pytest configuration and shared fixtures"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def activities_baseline():
    """Store the original activities state"""
    return deepcopy(activities)


@pytest.fixture
def client(activities_baseline):
    """
    Create a FastAPI TestClient with a fresh activities dict for each test.
    This fixture resets the activities dict to its baseline state after each test.
    """
    # Reset activities to baseline before test
    activities.clear()
    activities.update(activities_baseline)
    
    yield TestClient(app)
    
    # Clean up after test (optional, but good practice)
    activities.clear()
    activities.update(activities_baseline)
