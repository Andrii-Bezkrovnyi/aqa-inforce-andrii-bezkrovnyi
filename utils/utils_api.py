import json
import time
from datetime import datetime, timedelta
from pathlib import Path

import fake_useragent
import requests

from utils.test_data import (
    base_url,
    api_url,
    admin_credentials,
    valid_booking_data,
    invalid_booking_data,
    room_data
)
from utils.constants_ui import UIConstants
from loguru import logger

ua = fake_useragent.UserAgent()


class BookingUtils:
    """Utility class for common test operations and data management"""

    def __init__(self):
        self.test_data_file = "test_data.json"
        self.test_data_path = Path(__file__).resolve().parent / self.test_data_file
        self.test_data = self.get_test_data()
        self.base_url = self.test_data["base_url"]
        self.api_url = self.test_data.get("api_url", f"{self.base_url}/api/booking")
        self.admin_credentials = self.test_data["admin_credentials"]
        self.session = requests.Session()
        self.test_data.update({
            "valid_booking_data": valid_booking_data,
            "invalid_booking_data": invalid_booking_data,
            "room_data": room_data
        })

    def get_future_dates(self, days_from_now=None, checkout_days_later=None):
        """Method to get future check-in and check-out dates"""
        days_from_now = days_from_now or UIConstants.DEFAULT_CHECKIN_DAYS
        checkout_days_later = checkout_days_later or UIConstants.DEFAULT_CHECKOUT_DAYS
        checkin_date = datetime.now() + timedelta(days=days_from_now)
        checkout_date = checkin_date + timedelta(days=checkout_days_later)
        return {
            "checkin": checkin_date.strftime("%Y-%m-%d"),
            "checkout": checkout_date.strftime("%Y-%m-%d"),
            "checkin_day": checkin_date.day,
            "checkout_day": checkout_date.day,
            "checkin_month": checkin_date.month,
            "checkout_month": checkout_date.month
        }

    @property
    def room_api_base(self):
        """Returns the base URL for room operations (Admin API)"""
        return f"{self.base_url}/api/room"

    @property
    def booking_api_base(self):
        """Returns the base URL for booking operations (Public API)"""
        return f"{self.base_url}/api/booking"

    def get_test_data(self):
        """Load test data from JSON file or use fallback data"""
        try:
            with open(self.test_data_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.info(f"Warning: {self.test_data_file} not found, using fallback data")

            return {
                "base_url": base_url,
                "api_url": api_url,
                "admin_credentials": admin_credentials,
                "valid_booking_data": valid_booking_data,
                "invalid_booking_data": invalid_booking_data,
                "room_data": room_data
            }
        except json.JSONDecodeError as e:
            logger.info(f"Error: Invalid JSON in {self.test_data_file}: {e}")

            return {
                "base_url": base_url,
                "api_url": api_url,
                "admin_credentials": admin_credentials,
                "valid_booking_data": valid_booking_data,
                "invalid_booking_data": invalid_booking_data,
                "room_data": room_data
            }

    def get_admin_auth_token(self):
        """Get authentication token for admin operations"""
        try:
            login_url = f"{self.base_url}/api/auth/login"
            headers = {
                "Content-Type": "application/json",
                "User-Agent": ua.firefox
            }

            response = self.session.post(
                login_url,
                json=self.admin_credentials,
                headers=headers,
                timeout=30
            )

            if response.ok:
                data = response.json()
                return data.get("token")
            else:
                logger.info(
                    f"[API LOGIN FAIL] Status: {response.status_code},"
                    f" Response: {response.text}"
                )
        except Exception as exc:
            logger.info(f"[API LOGIN FAIL] Exception: {exc}")
        return None

    def create_test_room(self, room_data=None):
        """Create a test room and return room ID"""
        if not room_data:
            room_data = self.test_data["room_data"]

        token = self.get_admin_auth_token()
        if not token:
            raise Exception("Failed to get admin token")

        headers = {
            "Content-Type": "application/json",
            "Cookie": f"Bearer {token}",
            "User-Agent": ua.firefox
        }

        try:
            response = self.session.post(
                f"{self.base_url}/api/room",
                json=room_data,
                headers=headers,
                timeout=30
            )
            if response.status_code in [200, 201]:
                result = response.json()
                return result.get("roomid") or result.get("id")
            else:
                raise Exception(
                    f"Failed to create test room: Status {response.status_code}")
        except Exception as e:
            raise Exception(f"Failed to create test room: {e}")

    def delete_test_room(self, room_id):
        """Delete a test room"""
        token = self.get_admin_auth_token()
        if not token:
            return False

        headers = {
            "Content-Type": "application/json",
            "Cookie": f"Bearer {token}",
            "User-Agent": ua.firefox
        }

        try:
            response = self.session.delete(
                f"{self.base_url}/api/room/{room_id}",
                headers=headers,
                timeout=30
            )
            return response.status_code in [200, 202, 204]
        except Exception as e:
            logger.info(f"Failed to delete room {room_id}: {e}")
            return False

    def get_available_rooms(self):
        """Get list of available rooms"""
        try:
            headers = {
                "User-Agent": ua.firefox,
            }
            response = self.session.get(
                f"{self.base_url}/api/room/",
                headers=headers,
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("rooms", [])
        except Exception as e:
            logger.info(f"Failed to get rooms: {e}")
        return []

    def create_test_booking(self, room_id, booking_data):
        """Create a test booking and return booking ID"""
        if not booking_data:
            booking_data = self.test_data["valid_booking_data"]

        # days_from_now=30 is used to ensure the booking is always in the future
        dates = self.get_future_dates(days_from_now=30, checkout_days_later=1)

        payload = {
            "bookingdates": {
                "checkin": dates["checkin"],  # Using future check-in date
                "checkout": dates["checkout"]  # Using future check-out date
            },
            "roomid": room_id,
            "firstname": booking_data["firstname"],
            "lastname": booking_data["lastname"],
            "email": booking_data["email"],
            "phone": booking_data["phone"]
        }

        headers = {
            "Content-Type": "application/json",
            "Cookie": f"token={self.get_admin_auth_token()}",
            "User-Agent": ua.firefox
        }
        try:
            response = self.session.post(
                f"{self.base_url}/api/booking/",
                json=payload,
                headers=headers,
                timeout=30
            )
            logger.info(
                f"Booking creation status: "
                f"{response.status_code}, response: {response.text}"
            )
            if response.ok:
                result = response.json()
                booking_id = result.get("bookingid") or result.get("id")
                logger.info(f"Created booking ID: {booking_id}")
                return booking_id
            else:
                raise Exception(
                    f"Booking is not created: "
                    f"Status {response.status_code} - {response.text}"
                )
        except Exception as exc:
            raise Exception(f"Booking is not created: {exc}")

    def cleanup_test_rooms(self, api_base, headers):
        """Delete all rooms with 'Test' in their name"""
        try:
            response = self.session.get(api_base, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                rooms = data.get("rooms", [])
                for room in rooms:
                    room_name = room.get("roomName", "")
                    if "Test" in room_name:
                        room_id = room.get("roomid") or room.get("id")
                        if room_id:
                            self.session.delete(f"{api_base}/{room_id}",
                                                headers=headers, timeout=30)
                            time.sleep(1)  # Wait to avoid rate limiting
        except Exception as e:
            logger.info(f"Cleanup failed: {e}")

    def create_room(self, api_base, room_data, headers):
        """Create a room via API"""

        try:
            response = self.session.post(api_base, json=room_data, headers=headers,
                                         timeout=30)
            if response.ok:
                logger.info(f"Room created successfully: {response.json()}")
                return response.json()
            raise Exception(f"Failed to create room: Status {response.status_code}")
        except Exception as e:
            raise Exception(f"Failed to create room: {e}")

    def delete_room(self, api_base, room_id, headers):
        """Delete a room via API"""
        try:
            response = self.session.delete(
                f"{api_base}/{room_id}",
                headers=headers,
                timeout=30
            )
            return response.status_code in [200, 202, 204]
        except Exception as e:
            logger.info(f"Failed to delete room {room_id}: {e}")
            return False

    def create_booking(self, booking_api, booking_data):
        """Create a booking via API"""
        try:
            headers = {
                "Content-Type": "application/json",
                "User-Agent": ua.firefox
            }
            response = self.session.post(booking_api, json=booking_data,
                                         headers=headers, timeout=30)
            if response.status_code in [200, 201]:
                return response.json()
            raise Exception(
                f"Failed to create booking: "
                f"Status {response.status_code}, {response.text}"
            )
        except Exception as e:
            raise Exception(f"Failed to create booking: {e}")

    def delete_booking(self, booking_api, booking_id, headers):
        """Delete a booking via API"""
        try:
            response = self.session.delete(
                f"{booking_api}/{booking_id}",
                headers=headers,
                timeout=30
            )
            return response.status_code in [200, 202, 204]
        except Exception as e:
            logger.info(f"Failed to delete booking {booking_id}: {e}")
            return False

    def wait_for_api_response(
            self,
            url,
            method="GET",
            data=None,
            headers=None,
            timeout=30,
            retries=3
    ):
        """Wait for API response with retries"""
        for attempt in range(retries):
            try:
                if method.upper() == "GET":
                    response = self.session.get(
                        url,
                        headers=headers,
                        timeout=timeout)
                elif method.upper() == "POST":
                    response = self.session.post(
                        url,
                        json=data,
                        headers=headers,
                        timeout=timeout
                    )
                elif method.upper() == "DELETE":
                    response = self.session.delete(
                        url,
                        headers=headers,
                        timeout=timeout
                    )
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                return response

            except Exception as e:
                if attempt == retries - 1:
                    raise e
                time.sleep(1)  # Wait before retry

        return None

    def verify_room_exists(self, room_id):
        """Verify if a room exists by ID"""
        try:
            rooms = self.get_available_rooms()
            for room in rooms:
                if room.get("roomid") == room_id or room.get("id") == room_id:
                    return True
            return False
        except Exception as e:
            logger.info(f"Error during checking the room: {e}")
            return False

    def get_booking_details(self, booking_id):
        """Get booking details by ID"""
        try:
            token = self.get_admin_auth_token()
            if not token:
                logger.info("No admin token")
                return None

            headers = {
                "Content-Type": "application/json",
                "Cookie": f"token={token}",
                "User-Agent": "pytest"
            }

            url = f"{self.base_url}/api/booking/{booking_id}"
            logger.info(f"GET {url} with headers: {headers}")
            response = self.session.get(url, headers=headers, timeout=30)
            logger.info(f"Status code: {response.status_code}, Response: {response.text}")
            if response.status_code == 200:
                return response.json()
        except Exception as exc:
            logger.info(f"Failed to get booking details: {exc}")
        return None

    def update_room(self, room_id, room_data, headers):
        """Update room details via API"""
        try:
            # PUT request to update room
            response = self.session.put(
                f"{self.base_url}/api/room/{room_id}",
                json=room_data,
                headers=headers,
                timeout=30
            )
            if response.status_code in [200, 201, 202]:
                return response.json()
            raise Exception(f"Failed to update room: Status {response.status_code}")
        except Exception as e:
            raise Exception(f"Failed to update room: {e}")
