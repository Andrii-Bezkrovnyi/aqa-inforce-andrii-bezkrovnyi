import pytest


@pytest.mark.api
class TestAdminAPI:
    """Admin API Test Suite (Refactored)"""

    room_id = None
    booking_id = None

    def test_create_room(self, utils, admin_headers):
        """Test admin can create a new room"""
        api_base = utils.room_api_base
        room_data = utils.test_data["room_data"]
        # Create room (Admin API)
        utils.create_room(api_base, room_data, admin_headers)
        # Check the room is created successfully
        rooms = utils.get_available_rooms()
        matching_room = next(
            (room for room in rooms if room.get("roomName") == room_data["roomName"]),
            None
        )
        assert matching_room is not None, "Created room not found in room list"

        # Save room ID for later tests
        TestAdminAPI.room_id = matching_room.get("roomid")
        assert TestAdminAPI.room_id is not None

    def test_get_all_rooms(self, utils):
        """Test retrieving all rooms (User API)"""
        rooms = utils.get_available_rooms()
        assert isinstance(rooms, list), "Rooms should be returned as a list"
        assert any(room.get("roomid") == TestAdminAPI.room_id for room in
                   rooms), "Created room not found"

    def test_verify_created_room(self, utils):
        """Check that created room actually exists (User API)"""
        exists = utils.verify_room_exists(TestAdminAPI.room_id)
        assert exists, "Room not found after creation"

    def test_create_booking_room(self, utils):
        """Test admin can create a booking for a room"""
        booking_data = utils.test_data["valid_booking_data"]

        # Get room details to include in booking
        booking_id = utils.create_test_booking(TestAdminAPI.room_id, booking_data)
        assert booking_id, "Booking creation failed"

        # Save booking ID for later tests
        TestAdminAPI.booking_id = booking_id

    def test_get_booking_details(self, utils):
        """Test retrieving booking details (Admin API)"""
        booking = utils.get_booking_details(TestAdminAPI.booking_id)
        assert booking is not None, "Failed to fetch booking details"
        assert booking.get("bookingid") == TestAdminAPI.booking_id or booking.get(
            "id"
        ) == TestAdminAPI.booking_id

    def test_edit_room(self, utils, admin_headers):
        """Test: Edit Room (Admin API) and check changes (User API)"""
        updated_data = utils.test_data["room_data"].copy()
        updated_data["roomName"] = "Updated Room Name"
        updated_data["roomPrice"] = 999

        # Make the update (Admin API)
        result = utils.update_room(TestAdminAPI.room_id, updated_data, admin_headers)
        assert result is not None, "Update operation failed"

        # Check the changes (User API)
        rooms = utils.get_available_rooms()
        updated_room = next(
            (room for room in rooms if room["roomid"] == TestAdminAPI.room_id),
            None
        )

        assert updated_room is not None, "Room not found after update"
        assert updated_room["roomName"] == "Updated Room Name"
        assert updated_room["roomPrice"] == 999

    def test_delete_booking(self, utils, admin_headers):
        """Test deleting the created booking (Admin API)"""
        booking_api = utils.booking_api_base
        deleted = utils.delete_booking(
            booking_api,
            TestAdminAPI.booking_id,
            admin_headers
        )
        assert deleted, "Booking deletion failed"

    def test_delete_room(self, utils, admin_headers):
        """Test deleting the created room (Admin API)"""
        api_base = utils.room_api_base
        deleted = utils.delete_room(api_base, TestAdminAPI.room_id, admin_headers)
        assert deleted, "Room deletion failed"
