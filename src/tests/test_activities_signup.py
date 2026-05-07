"""Tests for POST/DELETE signup endpoints"""

import pytest


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup"""
    
    def test_signup_new_participant_success(self, client):
        """Test successfully signing up a new participant"""
        response = client.post(
            "/activities/Art%20Club/signup?email=newstudent@mergington.edu"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
    
    def test_signup_adds_participant_to_activity(self, client):
        """Test that signup actually adds participant to activity list"""
        # Get initial state
        response = client.get("/activities")
        initial_count = len(response.json()["Science Club"]["participants"])
        
        # Sign up new participant
        client.post("/activities/Science%20Club/signup?email=newsci@mergington.edu")
        
        # Verify participant was added
        response = client.get("/activities")
        data = response.json()
        assert len(data["Science Club"]["participants"]) == initial_count + 1
        assert "newsci@mergington.edu" in data["Science Club"]["participants"]
    
    def test_signup_activity_not_found(self, client):
        """Test signing up for non-existent activity returns 404"""
        response = client.post(
            "/activities/Nonexistent%20Club/signup?email=test@mergington.edu"
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]
    
    def test_signup_already_registered(self, client):
        """Test signing up when already registered returns 400"""
        email = "michael@mergington.edu"  # Already in Chess Club
        response = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()
    
    def test_signup_multiple_different_activities(self, client):
        """Test that same email can sign up for different activities"""
        email = "testperson@mergington.edu"
        
        # Sign up for first activity
        response1 = client.post(
            f"/activities/Art%20Club/signup?email={email}"
        )
        assert response1.status_code == 200
        
        # Sign up for different activity
        response2 = client.post(
            f"/activities/Science%20Club/signup?email={email}"
        )
        assert response2.status_code == 200
        
        # Verify both signups succeeded
        response = client.get("/activities")
        data = response.json()
        assert email in data["Art Club"]["participants"]
        assert email in data["Science Club"]["participants"]
    
    def test_signup_email_with_special_chars_encoded(self, client):
        """Test signup with URL-encoded email parameter"""
        # Email with plus sign (common in test emails)
        response = client.post(
            "/activities/Drama%20Club/signup?email=alice%2Btest@mergington.edu"
        )
        
        assert response.status_code == 200
        
        # Verify email was stored correctly
        response = client.get("/activities")
        data = response.json()
        assert "alice+test@mergington.edu" in data["Drama Club"]["participants"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup"""
    
    def test_unregister_participant_success(self, client):
        """Test successfully unregistering a participant"""
        email = "michael@mergington.edu"
        response = client.delete(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
    
    def test_unregister_removes_participant(self, client):
        """Test that unregister actually removes participant from list"""
        email = "ava@mergington.edu"  # In Drama Club
        
        # Get initial count
        response = client.get("/activities")
        initial_count = len(response.json()["Drama Club"]["participants"])
        
        # Unregister
        client.delete(f"/activities/Drama%20Club/signup?email={email}")
        
        # Verify removed
        response = client.get("/activities")
        data = response.json()
        assert len(data["Drama Club"]["participants"]) == initial_count - 1
        assert email not in data["Drama Club"]["participants"]
    
    def test_unregister_activity_not_found(self, client):
        """Test unregistering from non-existent activity returns 404"""
        response = client.delete(
            "/activities/Fake%20Club/signup?email=test@mergington.edu"
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]
    
    def test_unregister_email_not_in_activity(self, client):
        """Test unregistering email not in activity returns 400"""
        response = client.delete(
            "/activities/Chess%20Club/signup?email=notregistered@mergington.edu"
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"].lower()
    
    def test_signup_after_unregister(self, client):
        """Test that user can sign up again after unregistering"""
        email = "liam@mergington.edu"  # In Basketball Team
        
        # Unregister
        response = client.delete(
            f"/activities/Basketball%20Team/signup?email={email}"
        )
        assert response.status_code == 200
        
        # Verify removed
        response = client.get("/activities")
        assert email not in response.json()["Basketball Team"]["participants"]
        
        # Sign up again
        response = client.post(
            f"/activities/Basketball%20Team/signup?email={email}"
        )
        assert response.status_code == 200
        
        # Verify re-added
        response = client.get("/activities")
        assert email in response.json()["Basketball Team"]["participants"]


class TestDataIntegrity:
    """Tests for data consistency across operations"""
    
    def test_participant_count_consistency(self, client):
        """Test that participant count in response matches list length"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity in data.items():
            max_participants = activity["max_participants"]
            participant_count = len(activity["participants"])
            
            # Participant count should never exceed max
            assert participant_count <= max_participants
    
    def test_multiple_operations_state_preservation(self, client):
        """Test state consistency across multiple signup/unregister operations"""
        email1 = "user1@mergington.edu"
        email2 = "user2@mergington.edu"
        activity = "Art%20Club"
        
        # Sign up user1
        client.post(f"/activities/{activity}/signup?email={email1}")
        response = client.get("/activities")
        assert email1 in response.json()["Art Club"]["participants"]
        
        # Sign up user2
        client.post(f"/activities/{activity}/signup?email={email2}")
        response = client.get("/activities")
        data = response.json()
        assert email1 in data["Art Club"]["participants"]
        assert email2 in data["Art Club"]["participants"]
        
        # Unregister user1
        client.delete(f"/activities/{activity}/signup?email={email1}")
        response = client.get("/activities")
        data = response.json()
        assert email1 not in data["Art Club"]["participants"]
        assert email2 in data["Art Club"]["participants"]
