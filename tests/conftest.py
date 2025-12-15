import sys

import pytest
import requests
from loguru import logger

from utils.utils_api import BookingUtils
from utils.utils_ui import UIConstants


# Logger Setup
@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """Setup logging configuration for the test session."""
    # 1. Remove default logger
    logger.remove()

    # 2. Add console handler (for general info)
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )

    # 3. Add file handler (for detailed debug logs)
    log_file_path = "test_result_{time:YYYYMMDD}.log"
    logger.add(
        log_file_path,
        level="DEBUG",
        rotation="3 MB",
        compression="zip",
        enqueue=True,  # make logging asynchronous
        catch=True
    )
    logger.info("Logger configuration complete.")

    yield
    # logic to execute after all tests are done
    logger.info("Test session finished. Closing logs.")
    logger.complete()


# Class to hold context for UI tests
class TestContext:
    """
    Context for UI tests to hold page object and created booking IDs.
    """

    def __init__(self, page_obj):
        self.page = page_obj
        self.created_booking_ids = []


# Session-scoped fixture for BookingUtils
@pytest.fixture(scope="session")
def utils():
    """Initialize and provide BookingUtils instance for tests."""
    return BookingUtils()


@pytest.fixture(scope="session")
def admin_headers(utils):
    """Gет headers with admin auth token for API requests."""
    token = utils.get_admin_auth_token()
    assert token is not None, "Failed to retrieve admin token for fixture"

    # Headers for admin API requests
    return {
        "Content-Type": "application/json",
        "Cookie": f"token={token}",
        "User-Agent": "pytest"
    }


# Fixture for UI tests with setup and teardown
@pytest.fixture(scope="function")
def ui_app(page, utils):
    """
   Creates a test context for UI tests, navigates to the base URL,
   and cleans up created bookings after the test.
    """
    # --- SETUP PHASE ---
    base_url = utils.get_test_data()["base_url"]
    api_url = utils.get_test_data()["api_url"]

    # Navigates to the base URL
    page.goto(base_url)
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(UIConstants.TIMEOUT_PAGE_LOAD)

    # Create test context
    context = TestContext(page)

    # Give the test access to the context
    yield context

    # TEARDOWN PHASE (Cleanup)
    token = utils.get_admin_auth_token()

    # Delete created bookings if they exist
    if token and context.created_booking_ids:
        headers = {
            "Content-Type": "application/json",
            "Cookie": f"token={token}",
            "User-Agent": "pytest"
        }
        for booking_id in context.created_booking_ids:
            try:
                # Request to delete the booking
                requests.delete(
                    f"{api_url}/{booking_id}",
                    headers=headers,
                    timeout=10
                )
            except Exception as e:
                print(f"Failed to delete booking {booking_id} during cleanup: {e}")
