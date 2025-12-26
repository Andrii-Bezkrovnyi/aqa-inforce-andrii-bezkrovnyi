from page_object.base_page import BasePage
from utils.constants_ui import UIConstants


class HomePage(BasePage):
    """Methods for UI test helpers"""

    # Selectors for booking form elements used in filling the form
    BOOKING_ELEMENTS_SELECTORS = [
        'input[placeholder*="name"], input[name*="name"]',
        'input[type="email"], input[placeholder*="email"]',
        'input[type="tel"], input[placeholder*="phone"]',
        'button:has-text("Book"), input[value*="Book"]'
    ]

    @staticmethod
    def check_indicators(page):
        """Method to check for both success and error indicators on the page"""
        all_selectors = (
            BasePage.SUCCESS_INDICATORS_SELECTORS
            + BasePage.ERROR_INDICATORS_SELECTORS
        )
        combined_selector = ", ".join(all_selectors)
        # Check if any of the indicators are visible
        return page.locator(combined_selector).first.is_visible()

    @staticmethod
    def check_content_keywords(page, keywords):
        """Checking for keywords in the page content"""
        page_content = page.content()
        check_result = any(keyword in page_content.lower() for keyword in keywords)
        return check_result

    @staticmethod
    def count_booking_elements(page, timeout=UIConstants.TIMEOUT_RESPONSE):
        """
        Counts the number of booking elements on the page.
        """
        combined_selector = ", ".join(BasePage.BOOKING_ELEMENTS_SELECTORS)
        locator = page.locator(combined_selector)

        # Wait for at least one element to be visible within the timeout.
        # If none become visible, return 0 instead of throwing an exception.
        if locator.first.is_visible(timeout=timeout):
            return locator.count()
        return 0

    @staticmethod
    def click_element(page, selectors, timeout=UIConstants.TIMEOUT_RESPONSE):
        combined_selector = ", ".join(selectors)
        locator = page.locator(combined_selector).first

        # is_visible returns False if the element does not appear within the timeout
        if locator.is_visible(timeout=timeout):
            locator.click()
            return True
        return False

    @staticmethod
    def find_element_by_selectors(
            page,
            selectors,
            timeout=UIConstants.TIMEOUT_RESPONSE
    ):
        combined_selector = ", ".join(selectors)
        locator = page.locator(combined_selector).first
        # Wait for the element to be visible within the timeout.
        if locator.is_visible(timeout=timeout):
            return locator
        return None
