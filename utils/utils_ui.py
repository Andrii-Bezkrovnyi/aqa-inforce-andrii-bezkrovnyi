from page_object.page_object import UISelectors


class UIConstants:
    """Data constants for UI tests"""

    # Таймаути
    TIMEOUT_ELEMENTS = 10000
    TIMEOUT_CALENDAR = 3000
    TIMEOUT_RESPONSE = 3000
    TIMEOUT_PAGE_LOAD = 3000
    TIMEOUT_INTERACTION = 2000
    TIMEOUT_FORM_SUBMIT = 2000
    TIMEOUT_CALENDAR_INTERACTION = 1000
    TIMEOUT_MOUSE_MOVE = 1000
    TIMEOUT_ADDITIONAL_WAIT = 5000

    # Default booking dates
    DEFAULT_CHECKIN_DAYS = 7
    DEFAULT_CHECKOUT_DAYS = 2
    TEST_BOOKING_CHECKIN = "2026-12-12"
    TEST_BOOKING_CHECKOUT = "2026-12-16"

    # Success keywords for content verification
    SUCCESS_KEYWORDS = ['booking', 'confirmed', 'success', 'thank']

    # Error keywords for content verification
    ERROR_KEYWORDS = ['error', 'invalid', 'required', 'empty']

    # Minimal content length for page validation
    MIN_PAGE_CONTENT_LENGTH = 100

    # Data for API booking tests
    API_TEST_BOOKING_DATA = {
        "firstname": "Andrii",
        "lastname": "Test",
        "email": "andrii@example.com",
        "phone": "09718618291",
        "bookingdates": {
            "checkin": TEST_BOOKING_CHECKIN,
            "checkout": TEST_BOOKING_CHECKOUT
        }
    }


class UIHelpers:
    """Methods for UI test helpers"""

    @staticmethod
    def format_date_selector(template, day=None, date=None):
        """Creates a formatted date selector string"""
        if day:
            return template.format(day=day)
        if date:
            return template.format(date=date)
        return template

    @staticmethod
    def get_calendar_selectors(day):
        """Returns a list of calendar date selectors with a specific day"""
        return [
            UIHelpers.format_date_selector(selector, day=day)
            for selector in UISelectors.CALENDAR_DATE_SELECTORS
        ]

    @staticmethod
    def get_unavailable_date_selectors(day):
        """Returns a list of unavailable date selectors with a specific day"""
        return [
            UIHelpers.format_date_selector(selector, day=day)
            for selector in UISelectors.UNAVAILABLE_DATE_SELECTORS
        ]

    @staticmethod
    def check_success_indicators(page):
        """Checking success indicators on the page"""
        for indicator in UISelectors.SUCCESS_INDICATORS_SELECTORS:
            try:
                if page.locator(indicator).count() > 0:
                    return True
            except:
                continue
        return False

    @staticmethod
    def check_error_indicators(page):
        """Checks for error indicators on the page"""
        for indicator in UISelectors.ERROR_INDICATORS_SELECTORS:
            try:
                if page.locator(indicator).count() > 0:
                    return True
            except:
                continue
        return False

    @staticmethod
    def check_content_keywords(page, keywords):
        """Checking for keywords in the page content"""
        try:
            page_content = page.content()
            return any(keyword in page_content.lower() for keyword in keywords)
        except:
            return False

    @staticmethod
    def count_booking_elements(page):
        """Counts the number of booking-related elements found on the page"""
        elements_found = 0
        for selector in UISelectors.BOOKING_ELEMENTS_SELECTORS:
            try:
                if page.locator(selector).count() > 0:
                    elements_found += 1
            except:
                continue
        return elements_found

    @staticmethod
    def click_element(page, selectors):
        """Clicks an element from a list of selectors if found"""
        for selector in selectors:
            try:
                element = page.locator(selector).first
                if element.count() > 0:
                    element.click()
                    return True
            except:
                continue
        return False

    @staticmethod
    def find_element_by_selectors(page, selectors):
        """Finds and returns the first matching element from a list of selectors"""
        for selector in selectors:
            try:
                element = page.locator(selector).first
                if element.count() > 0:
                    return element
            except:
                continue
        return None
