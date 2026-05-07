"""Tests for GET /activities endpoint"""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify all activities are returned
    assert isinstance(data, dict)
    assert len(data) > 0
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Debate Team" in data


def test_get_activities_response_structure(client):
    """Test that activity objects have the correct structure"""
    response = client.get("/activities")
    data = response.json()
    
    # Check structure of an activity
    activity = data["Chess Club"]
    required_fields = {"description", "schedule", "max_participants", "participants"}
    assert required_fields.issubset(activity.keys())
    
    # Verify field types
    assert isinstance(activity["description"], str)
    assert isinstance(activity["schedule"], str)
    assert isinstance(activity["max_participants"], int)
    assert isinstance(activity["participants"], list)


def test_get_activities_initial_participants(client):
    """Test that initial participant counts are correct"""
    response = client.get("/activities")
    data = response.json()
    
    # Verify known initial state
    chess_club = data["Chess Club"]
    assert len(chess_club["participants"]) == 2
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]
    
    programming = data["Programming Class"]
    assert len(programming["participants"]) == 2
    assert "emma@mergington.edu" in programming["participants"]
