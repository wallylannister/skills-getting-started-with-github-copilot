"""
Integration tests for Mergington High School API endpoints.

All tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and fixtures
- Act: Make HTTP requests to the API
- Assert: Verify status codes and response payloads
"""

import pytest


class TestRootEndpoint:
    """Test cases for the GET / endpoint"""

    def test_root_redirects_to_index(self, client):
        """
        Test that GET / redirects to /static/index.html
        
        Arrange: TestClient fixture is ready
        Act: Make GET request to /
        Assert: Verify redirect status code and location header
        """
        # Arrange: (fixture provides client)
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers.get("location", "")


class TestActivitiesEndpoint:
    """Test cases for the GET /activities endpoint"""

    def test_get_all_activities_returns_nine_activities(self, client):
        """
        Test that GET /activities returns all 9 activities
        
        Arrange: TestClient fixture is ready
        Act: Make GET request to /activities
        Assert: Verify response contains exactly 9 activities with correct structure
        """
        # Arrange: (fixture provides client)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities

    def test_activity_has_required_fields(self, client):
        """
        Test that each activity has required fields: description, schedule, max_participants, participants
        
        Arrange: TestClient fixture is ready
        Act: Make GET request to /activities
        Assert: Verify each activity contains all required fields
        """
        # Arrange: (fixture provides client)
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert required_fields.issubset(activity_data.keys()), \
                f"Activity {activity_name} missing required fields"

    def test_participants_is_list_of_emails(self, client):
        """
        Test that participants field is a list of email strings
        
        Arrange: TestClient fixture is ready
        Act: Make GET request to /activities
        Assert: Verify participants field is a list with email strings
        """
        # Arrange: (fixture provides client)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list), \
                f"Activity {activity_name} participants is not a list"
            for participant in activity_data["participants"]:
                assert isinstance(participant, str), \
                    f"Participant in {activity_name} is not a string"
                assert "@" in participant, \
                    f"Participant {participant} in {activity_name} is not a valid email format"


class TestSignupEndpoint:
    """Test cases for the POST /activities/{activity_name}/signup endpoint"""

    def test_signup_new_student_success(self, client, activity_name, new_participant_email):
        """
        Test successful signup of a new student to an activity
        
        Arrange: Use test fixtures for activity name and new participant email
        Act: Make POST request to signup endpoint with valid activity and email
        Assert: Verify success response and participant added to activity
        """
        # Arrange
        initial_response = client.get(f"/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_participant_email}
        )
        
        # Assert
        assert response.status_code == 200
        assert new_participant_email in response.json()["message"]
        
        # Verify participant was added
        verify_response = client.get("/activities")
        final_count = len(verify_response.json()[activity_name]["participants"])
        assert final_count == initial_count + 1

    def test_signup_nonexistent_activity_returns_404(self, client, invalid_activity_name, new_participant_email):
        """
        Test that signup to a non-existent activity returns 404 error
        
        Arrange: Use invalid activity name fixture
        Act: Make POST request with non-existent activity name
        Assert: Verify 404 status code and appropriate error message
        """
        # Arrange: (fixtures provided)
        
        # Act
        response = client.post(
            f"/activities/{invalid_activity_name}/signup",
            params={"email": new_participant_email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_email_returns_400(self, client, activity_name, existing_participant_email):
        """
        Test that signing up with a duplicate email returns 400 error
        
        Arrange: Use existing participant email that's already signed up to Chess Club
        Act: Try to sign up the same email again
        Assert: Verify 400 status code and duplicate signup error message
        """
        # Arrange: (fixture provides existing participant already in Chess Club)
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_participant_email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_missing_email_param_returns_error(self, client, activity_name):
        """
        Test that signup without email parameter returns error
        
        Arrange: Prepare request without email parameter
        Act: Make POST request without email param
        Assert: Verify error response (either 422 or 400 depending on FastAPI validation)
        """
        # Arrange: (fixture provides activity name)
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup")
        
        # Assert
        assert response.status_code in [400, 422]  # 422 for validation error, 400 for missing param


class TestRemoveParticipantEndpoint:
    """Test cases for the DELETE /activities/{activity_name}/participants/{email} endpoint"""

    def test_remove_existing_participant_success(self, client, activity_name, existing_participant_email):
        """
        Test successful removal of an existing participant
        
        Arrange: Use existing participant email fixture
        Act: Make DELETE request to remove participant
        Assert: Verify success response and participant removed from activity
        """
        # Arrange
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        assert existing_participant_email in initial_response.json()[activity_name]["participants"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{existing_participant_email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert existing_participant_email in response.json()["message"]
        
        # Verify participant was removed
        verify_response = client.get("/activities")
        final_count = len(verify_response.json()[activity_name]["participants"])
        assert final_count == initial_count - 1
        assert existing_participant_email not in verify_response.json()[activity_name]["participants"]

    def test_remove_from_nonexistent_activity_returns_404(self, client, invalid_activity_name, sample_email):
        """
        Test that removing from a non-existent activity returns 404 error
        
        Arrange: Use invalid activity name fixture
        Act: Make DELETE request with non-existent activity name
        Assert: Verify 404 status code and appropriate error message
        """
        # Arrange: (fixtures provided)
        
        # Act
        response = client.delete(
            f"/activities/{invalid_activity_name}/participants/{sample_email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_remove_nonexistent_participant_returns_400(self, client, activity_name, new_participant_email):
        """
        Test that removing a participant not signed up returns 400 error
        
        Arrange: Use new participant email that's not signed up to the activity
        Act: Try to remove the participant
        Assert: Verify 400 status code and error message
        """
        # Arrange: (new_participant_email is not signed up by default)
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{new_participant_email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]


class TestEndpointIntegration:
    """Integration tests combining multiple endpoints"""

    def test_signup_then_remove_workflow(self, client, activity_name, new_participant_email):
        """
        Test complete workflow: signup a student, verify they're in the activity, then remove them
        
        Arrange: Prepare activity and new participant
        Act: Sign up, verify, and then remove
        Assert: Verify each step succeeds and final state is correct
        """
        # Arrange
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_participant_email}
        )
        assert signup_response.status_code == 200
        
        # Act: Verify signup
        activities = client.get("/activities").json()
        assert new_participant_email in activities[activity_name]["participants"]
        
        # Act: Remove
        remove_response = client.delete(
            f"/activities/{activity_name}/participants/{new_participant_email}"
        )
        
        # Assert
        assert remove_response.status_code == 200
        final_activities = client.get("/activities").json()
        assert new_participant_email not in final_activities[activity_name]["participants"]
