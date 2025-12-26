class BasePage:
    """Selectors for UI testing of the hotel booking application."""
    # Selectors for submit buttons
    SUBMIT_BUTTON_SELECTORS = [
        'button[type="submit"]',
        'input[type="submit"]',
        'button:has-text("Submit")',
        'button:has-text("Book")',
        '.btn-primary',
        '.submit-btn'
    ]
    # Selectors for room loading indicators
    ROOMS_LOADING_SELECTORS = [
        '.row.hotel-room-info',
        '.room',
        '[class*="room"]'
    ]

    # Selectors for success indicators
    SUCCESS_INDICATORS_SELECTORS = [
        'text="Booking Successful"',
        'text="Booking confirmed"',
        'text="Thank you"',
        '.alert-success',
        '.success-message',
        '[class*="success"]'
    ]

    # Selectors for error indicators
    ERROR_INDICATORS_SELECTORS = [
        '.alert-danger',
        '.error-message',
        '[class*="error"]',
        'text="must not be empty"',
        'text="must be a well-formed email"',
        'text="must not be null"'
    ]
    # Selectors for booking form elements used in filling the form
    BOOKING_ELEMENTS_SELECTORS = [
        'input[placeholder*="name"], input[name*="name"]',
        'input[type="email"], input[placeholder*="email"]',
        'input[type="tel"], input[placeholder*="phone"]',
        'button:has-text("Book"), input[value*="Book"]'
    ]
