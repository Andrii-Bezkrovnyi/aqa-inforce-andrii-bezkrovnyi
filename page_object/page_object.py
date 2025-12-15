class UISelectors:
    """Selectors for UI testing of the hotel booking application."""

    # Selectors for room loading indicators
    ROOMS_LOADING_SELECTORS = [
        '.row.hotel-room-info',
        '.room',
        '[class*="room"]'
    ]

    # Selectors for booking form fields
    BOOKING_FORM_SELECTORS = {
        'firstname': [
            'input[placeholder*="Firstname"]',
            'input[name="firstname"]',
            'input#firstname',
            '.firstname input'
        ],
        'lastname': [
            'input[placeholder*="Lastname"]',
            'input[name="lastname"]',
            'input#lastname',
            '.lastname input'
        ],
        'email': [
            'input[placeholder*="Email"]',
            'input[name="email"]',
            'input#email',
            '.email input',
            'input[type="email"]'
        ],
        'phone': [
            'input[placeholder*="Phone"]',
            'input[name="phone"]',
            'input#phone',
            '.phone input',
            'input[type="tel"]'
        ],
        'checkin': [
            'input[placeholder*="Check-in"]',
            'input[name="checkin"]',
            'input#checkin',
            '.checkin input'
        ],
        'checkout': [
            'input[placeholder*="Check-out"]',
            'input[name="checkout"]',
            'input#checkout',
            '.checkout input'
        ],
        'book_button': [
            'button:has-text("Book")',
            '.btn:has-text("Book")',
            'input[type="submit"][value*="Book"]'
        ]
    }

    # Bocking button selectors
    BOOKING_BUTTON_SELECTORS = [
        'button:has-text("Book")',
        '.btn:has-text("Book")',
        'input[value*="Book"]'
    ]

    # Selectors for submit buttons
    SUBMIT_BUTTON_SELECTORS = [
        'button[type="submit"]',
        'input[type="submit"]',
        'button:has-text("Submit")',
        'button:has-text("Book")',
        '.btn-primary',
        '.submit-btn'
    ]

    # Calendar date selectors
    CALENDAR_DATE_SELECTORS = [
        'button:has-text("{day}")',
        '.day:has-text("{day}")',
        '[data-date*="{date}"]'
    ]

    # Selectors for unavailable dates in the calendar
    UNAVAILABLE_DATE_SELECTORS = [
        'button:has-text("{day}")[disabled]',
        '.disabled:has-text("{day}")',
        '.unavailable:has-text("{day}")'
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
