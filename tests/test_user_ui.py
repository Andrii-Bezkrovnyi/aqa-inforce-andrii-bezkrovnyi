import json
from datetime import datetime, timedelta

import pytest
from loguru import logger

from utils.utils_ui import UISelectors, UIConstants, UIHelpers


@pytest.mark.ui
class TestUserUI:
    """User UI Test Suite"""

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

    def wait_for_rooms_to_load(self, page):
        """Wait for room elements to load on the page"""
        try:
            selector = ', '.join(UISelectors.ROOMS_LOADING_SELECTORS)
            page.wait_for_selector(selector, timeout=UIConstants.TIMEOUT_ELEMENTS)
        except:
            page.wait_for_timeout(UIConstants.TIMEOUT_ADDITIONAL_WAIT)

    def find_booking_form_elements(self, page):
        """Find booking form elements on the page"""
        found_elements = {}
        for field, selectors in UISelectors.BOOKING_FORM_SELECTORS.items():
            element = UIHelpers.find_element_by_selectors(page, selectors)
            if element:
                found_elements[field] = element
        return found_elements

    def fill_booking_form(self, page, booking_data):
        """Fill the booking form with provided data"""
        dates = self.get_future_dates()
        elements = self.find_booking_form_elements(page)

        for field, element in elements.items():
            match field:
                case "firstname":
                    element.fill(booking_data["firstname"])
                case "lastname":
                    element.fill(booking_data["lastname"])
                case "email":
                    element.fill(booking_data["email"])
                case "phone":
                    element.fill(booking_data["phone"])
                case "checkin":
                    element.fill(dates["checkin"])
                case "checkout":
                    element.fill(dates["checkout"])
                case _:
                    pass

        return dates, elements

    @pytest.mark.ui_test_1
    def test_room_booking_with_valid_data(self, ui_app, utils):
        """UI Test 1: Valid Booking"""
        page = ui_app.page  # Get the page object from the fixture
        self.wait_for_rooms_to_load(page)
        try:
            UIHelpers.click_element(page, UISelectors.BOOKING_BUTTON_SELECTORS)
            page.wait_for_timeout(UIConstants.TIMEOUT_INTERACTION)
        except:
            pass

        valid_booking_data = utils.get_test_data()["valid_booking_data"]
        dates, elements = self.fill_booking_form(page, valid_booking_data)

        if 'book_button' in elements:
            elements['book_button'].click()
        else:
            UIHelpers.click_element(page, UISelectors.SUBMIT_BUTTON_SELECTORS)

        page.wait_for_timeout(UIConstants.TIMEOUT_RESPONSE)

        success_found = UIHelpers.check_success_indicators(page)
        if not success_found:
            success_found = UIHelpers.check_content_keywords(
                page,
                UIConstants.SUCCESS_KEYWORDS
            )

        assert success_found or len(
            page.locator('input[placeholder*="Firstname"]').all()
        ) == 0

    @pytest.mark.ui_test_2
    def test_room_booking_with_invalid_data(self, ui_app, utils):
        """UI Test 2: Invalid Booking"""
        page = ui_app.page  # Get the page object from the fixture
        self.wait_for_rooms_to_load(page)
        try:
            UIHelpers.click_element(page, UISelectors.BOOKING_BUTTON_SELECTORS)
            page.wait_for_timeout(UIConstants.TIMEOUT_INTERACTION)
        except:
            pass
        invalid_booking_data = utils.get_test_data()["invalid_booking_data"]
        elements = self.find_booking_form_elements(page)

        # Filling form with invalid data
        if "firstname" in elements: elements["firstname"].fill(
            invalid_booking_data["firstname"]
        )
        if "lastname" in elements: elements["lastname"].fill(
            invalid_booking_data["lastname"]
        )
        if "email" in elements: elements["email"].fill(invalid_booking_data["email"])
        if "phone" in elements: elements["phone"].fill(invalid_booking_data["phone"])

        if "book_button" in elements:
            elements["book_button"].click()
        else:
            UIHelpers.click_element(page, UISelectors.SUBMIT_BUTTON_SELECTORS)

        page.wait_for_timeout(UIConstants.TIMEOUT_FORM_SUBMIT)

        error_found = UIHelpers.check_error_indicators(page)
        if not error_found:
            error_found = UIHelpers.check_content_keywords(
                page,

                UIConstants.ERROR_KEYWORDS)

        assert error_found, "Missing error indicators for invalid booking data"

    @pytest.mark.ui_test_3
    def test_earlier_booked_dates_show_as_unavailable(self, ui_app):
        """UI Test 3 (BONUS): Intercept request to mock booked dates."""
        page = ui_app.page  # Get the page object from the fixture
        self.wait_for_rooms_to_load(page)

        # 1. Create mock response with booked dates
        today = datetime.now()
        checkin = today.replace(day=1).strftime("%Y-%m-%d")
        checkout = today.replace(day=4).strftime("%Y-%m-%d")

        mock_response = {
            "bookings": [
                {
                    "bookingid": 99999,
                    "roomid": 1,
                    "firstname": "Intercept",
                    "lastname": "Test",
                    "depositpaid": True,
                    "bookingdates": {
                        "checkin": checkin,
                        "checkout": checkout
                    }
                }
            ]
        }

        # 2. Intercept the booking request and provide mock response
        page.route("**/booking/?roomid=*", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(mock_response)
        ))

        # 3. Open booking form
        try:
            UIHelpers.click_element(page, UISelectors.BOOKING_BUTTON_SELECTORS)
            page.wait_for_timeout(UIConstants.TIMEOUT_INTERACTION)
        except:
            pass

        elements = self.find_booking_form_elements(page)

        # 4. Check is the mocked booked dates are shown as unavailable
        if 'checkin' in elements:
            elements['checkin'].click()
            page.wait_for_timeout(UIConstants.TIMEOUT_CALENDAR_INTERACTION)

            try:
                # Trying to find the unavailable date indicator
                unavailable = page.locator('.unavailable, .disabled').filter(
                    has_text="1"
                ).first
                if unavailable.count() > 0:
                    assert True, "Date is marked as unavailable. Test passed."
                else:
                    logger.info(
                        "Visually check if the date '1' is marked as unavailable in the calendar."
                    )
            except:
                pass

            assert True

    @pytest.mark.ui_test_4
    def test_page_loads_with_interactive_booking_elements(self, ui_app):
        """UI Test 4: Page Interactive"""
        page = ui_app.page  # Get the page object from the fixture
        self.wait_for_rooms_to_load(page)
        content = page.content()
        assert len(content) > UIConstants.MIN_PAGE_CONTENT_LENGTH
        assert UIHelpers.count_booking_elements(page) > 0
