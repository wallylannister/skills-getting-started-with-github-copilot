"""
Pytest configuration and fixtures for Mergington High School API tests.

Provides reusable test fixtures following the AAA pattern (Arrange-Act-Assert):
- client: FastAPI TestClient for making HTTP requests
- sample_email: Standard test email for signup/removal tests
- mock_activities: Sample activity data for testing

Note: The activities_reset fixture ensures test isolation by resetting the shared
activities dictionary to its initial state before each test.
"""

import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


# Store the initial state of activities at import time
INITIAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture that automatically resets the activities state before each test.
    
    This ensures test isolation by restoring the activities dictionary to its initial state.
    The 'autouse=True' parameter means this fixture runs before every test automatically.
    
    Used in the Arrange phase to ensure consistent initial state.
    """
    # Reset to initial state before the test
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))
    yield
    # Could add cleanup here if needed


@pytest.fixture
def client():
    """
    Fixture that provides a FastAPI TestClient.
    
    Used in the Arrange phase of tests to set up a test client
    that allows making HTTP requests to the app without running a server.
    """
    return TestClient(app)


@pytest.fixture
def sample_email():
    """
    Fixture providing a standard test email address.
    
    Used in test Arrange phase for consistent email values
    across multiple tests.
    """
    return "test.student@mergington.edu"


@pytest.fixture
def new_participant_email():
    """
    Fixture providing an email for a new participant not yet signed up.
    
    Used in test Arrange phase for signup tests.
    """
    return "new.student@mergington.edu"


@pytest.fixture
def existing_participant_email():
    """
    Fixture providing an email for an existing participant already signed up.
    
    Used in test Arrange phase. This corresponds to an existing participant
    in the Chess Club activity (see app.py).
    """
    return "michael@mergington.edu"


@pytest.fixture
def activity_name():
    """
    Fixture providing a valid activity name.
    
    Used in test Arrange phase for endpoint tests.
    """
    return "Chess Club"


@pytest.fixture
def invalid_activity_name():
    """
    Fixture providing an invalid activity name that doesn't exist.
    
    Used in test Arrange phase for error case tests.
    """
    return "Non-existent Activity"
