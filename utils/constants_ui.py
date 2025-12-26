class UIConstants:
    """Data constants for UI tests"""

    # Timeout values in milliseconds
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
