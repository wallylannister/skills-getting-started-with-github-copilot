"""
Unit tests for Mergington High School API data structures and business logic.

All tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and test conditions
- Act: Invoke functions or access data structures
- Assert: Verify the results and side effects
"""

import pytest
from src.app import activities


class TestActivityDataStructure:
    """Test cases for activity data structure validation"""

    def test_activities_dictionary_contains_nine_activities(self):
        """
        Test that the activities dictionary has exactly 9 activities
        
        Arrange: Import activities dictionary
        Act: Check length of activities dict
        Assert: Verify exactly 9 activities exist
        """
        # Arrange: (activities module imported)
        
        # Act
        activity_count = len(activities)
        
        # Assert
        assert activity_count == 9

    def test_all_activity_names_are_strings(self):
        """
        Test that all activity names (keys) are strings
        
        Arrange: Import activities dictionary
        Act: Check type of each key
        Assert: Verify all keys are strings
        """
        # Arrange: (activities module imported)
        
        # Act & Assert
        for activity_name in activities.keys():
            assert isinstance(activity_name, str), \
                f"Activity name {activity_name} is not a string"

    def test_all_activities_have_required_fields(self):
        """
        Test that each activity contains all required fields
        
        Arrange: Define required fields
        Act: Iterate through each activity
        Assert: Verify each activity has description, schedule, max_participants, participants
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act & Assert
        for activity_name, activity_data in activities.items():
            assert required_fields.issubset(activity_data.keys()), \
                f"Activity '{activity_name}' missing required fields"

    def test_description_is_string(self):
        """
        Test that description field is a string for all activities
        
        Arrange: Import activities dictionary
        Act: Check type of description field
        Assert: Verify all descriptions are strings
        """
        # Arrange: (activities module imported)
        
        # Act & Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["description"], str), \
                f"Activity '{activity_name}' description is not a string"
            assert len(activity_data["description"]) > 0, \
                f"Activity '{activity_name}' description is empty"

    def test_schedule_is_string(self):
        """
        Test that schedule field is a string for all activities
        
        Arrange: Import activities dictionary
        Act: Check type of schedule field
        Assert: Verify all schedules are strings
        """
        # Arrange: (activities module imported)
        
        # Act & Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["schedule"], str), \
                f"Activity '{activity_name}' schedule is not a string"
            assert len(activity_data["schedule"]) > 0, \
                f"Activity '{activity_name}' schedule is empty"

    def test_max_participants_is_positive_integer(self):
        """
        Test that max_participants field is a positive integer for all activities
        
        Arrange: Import activities dictionary
        Act: Check type and value of max_participants
        Assert: Verify all max_participants are positive integers
        """
        # Arrange: (activities module imported)
        
        # Act & Assert
        for activity_name, activity_data in activities.items():
            max_participants = activity_data["max_participants"]
            assert isinstance(max_participants, int), \
                f"Activity '{activity_name}' max_participants is not an integer"
            assert max_participants > 0, \
                f"Activity '{activity_name}' max_participants is not positive"

    def test_participants_is_list_of_strings(self):
        """
        Test that participants field is a list of email strings
        
        Arrange: Import activities dictionary
        Act: Check type of participants and each element
        Assert: Verify participants is a list with email strings
        """
        # Arrange: (activities module imported)
        
        # Act & Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list), \
                f"Activity '{activity_name}' participants is not a list"
            for participant in activity_data["participants"]:
                assert isinstance(participant, str), \
                    f"Participant in '{activity_name}' is not a string"


class TestActivityParticipantCount:
    """Test cases for participant count constraints"""

    def test_participant_count_does_not_exceed_max(self):
        """
        Test that no activity has more participants than max_participants
        
        Arrange: Import activities dictionary
        Act: Compare participant count with max_participants
        Assert: Verify no activity exceeds its max capacity
        """
        # Arrange: (activities module imported)
        
        # Act & Assert
        for activity_name, activity_data in activities.items():
            participant_count = len(activity_data["participants"])
            max_participants = activity_data["max_participants"]
            assert participant_count <= max_participants, \
                f"Activity '{activity_name}' has {participant_count} participants but max is {max_participants}"

    def test_all_participants_have_email_format(self):
        """
        Test that all participant emails follow a basic email format
        
        Arrange: Import activities dictionary
        Act: Check each participant email
        Assert: Verify all emails contain @ symbol
        """
        # Arrange: (activities module imported)
        
        # Act & Assert
        for activity_name, activity_data in activities.items():
            for participant in activity_data["participants"]:
                assert "@" in participant, \
                    f"Invalid email format for participant '{participant}' in '{activity_name}'"

    def test_no_duplicate_participants_in_activity(self):
        """
        Test that each activity has no duplicate participants
        
        Arrange: Import activities dictionary
        Act: Compare participant list length with set length
        Assert: Verify no duplicates exist
        """
        # Arrange: (activities module imported)
        
        # Act & Assert
        for activity_name, activity_data in activities.items():
            participants = activity_data["participants"]
            unique_participants = set(participants)
            assert len(participants) == len(unique_participants), \
                f"Activity '{activity_name}' has duplicate participants"


class TestSpecificActivities:
    """Test cases for specific activities and their properties"""

    def test_chess_club_exists(self):
        """
        Test that Chess Club activity exists
        
        Arrange: Import activities dictionary
        Act: Check for Chess Club key
        Assert: Verify Chess Club exists
        """
        # Arrange: (activities module imported)
        
        # Act & Assert
        assert "Chess Club" in activities

    def test_programming_class_exists(self):
        """
        Test that Programming Class activity exists
        
        Arrange: Import activities dictionary
        Act: Check for Programming Class key
        Assert: Verify Programming Class exists
        """
        # Arrange: (activities module imported)
        
        # Act & Assert
        assert "Programming Class" in activities

    def test_chess_club_has_initial_participants(self):
        """
        Test that Chess Club has at least 2 initial participants
        
        Arrange: Import activities dictionary
        Act: Get Chess Club participants
        Assert: Verify it has participants
        """
        # Arrange: (activities module imported)
        
        # Act
        chess_club = activities["Chess Club"]
        participant_count = len(chess_club["participants"])
        
        # Assert
        assert participant_count >= 2, \
            f"Chess Club has {participant_count} participants, expected at least 2"
