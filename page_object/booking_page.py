from datetime import datetime, timedelta

from page_object.base_page import BasePage
from utils.constants_ui import UIConstants


class BookingComponent(BasePage):
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
    # Bocking button selectors
    BOOKING_BUTTON_SELECTORS = [
        'button:has-text("Book")',
        '.btn:has-text("Book")',
        'input[value*="Book"]'
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

    def wait_for_rooms_to_load(self, page):
        """Wait for room elements to load on the page"""
        selector = ', '.join(self.ROOMS_LOADING_SELECTORS)
        page.wait_for_selector(selector, timeout=UIConstants.TIMEOUT_ELEMENTS)

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

    def find_booking_form_elements(self, page):
        """Find booking form elements on the page"""
        from page_object.home_page import HomePage
        found_elements = {}
        for field, selectors in BookingComponent.BOOKING_FORM_SELECTORS.items():
            element = HomePage.find_element_by_selectors(page, selectors)
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
            BookingComponent.format_date_selector(selector, day=day)
            for selector in BookingComponent.CALENDAR_DATE_SELECTORS
        ]

    @staticmethod
    def get_unavailable_date_selectors(day):
        """Returns a list of unavailable date selectors with a specific day"""
        return [
            BookingComponent.format_date_selector(selector, day=day)
            for selector in BookingComponent.UNAVAILABLE_DATE_SELECTORS
        ]
