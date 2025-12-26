import sys

import pytest
import requests
from loguru import logger

from page_object.booking_page import BookingComponent
from page_object.home_page import HomePage
from utils.utils_api import BookingUtils


# Logger Setup
@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    logger.remove()
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
               " - <level>{message}</level>",
        colorize=True
    )
    log_file_path = "test_result_{time:YYYYMMDD}.log"
    logger.add(
        log_file_path,
        level="DEBUG",
        rotation="3 MB",
        compression="zip",
        enqueue=True,
        catch=True
    )
    logger.info("Logger configuration complete.")
    yield
    logger.info("Test session finished. Closing logs.")
    logger.complete()


# Context Class for UI Tests
class TestContext:
    def __init__(self, page_obj):
        self.page = page_obj
        self.created_booking_ids = []


@pytest.fixture
def home_page(page):
    return HomePage()


@pytest.fixture
def booking_page(page):
    return BookingComponent()


@pytest.fixture(scope="session")
def utils():
    return BookingUtils()


# Admin Headers Fixture
@pytest.fixture(scope="session")
def admin_headers(utils):
    token = utils.get_admin_auth_token()
    assert token is not None, "Failed to retrieve admin token for fixture"
    return {
        "Content-Type": "application/json",
        "Cookie": f"token={token}",
        "User-Agent": "pytest"
    }


# Browser Configuration Fixtures
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Settings for browser launch."""
    return {
        **browser_type_launch_args,
        "headless": True,  # Set to False for debugging
        "args": [
            "--start-maximized",
            "--no-sandbox",
            "--disable-setuid-sandbox"
        ]
    }


# Browser Context Fixture
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Settings for browser context.
    no_viewport set to True to use full available screen size.
    """
    return {
        **browser_context_args,
        "viewport": None,
        "no_viewport": True
    }


# Main UI App Fixture
@pytest.fixture(scope="function")
def ui_app(page, utils):
    """
    Creates a UI test context, navigates to the base URL,
    and handles cleanup of created bookings after the test.
    """
    #  SETUP PHASE
    logger.info("UI Test Setup: Navigating to base URL")
    screen_size = page.evaluate(
        "() => ({width: window.screen.availWidth, height: window.screen.availHeight})"
    )
    logger.info(
        f"Detected screen resolution: {screen_size['width']}x{screen_size['height']}"
    )
    base_url = utils.get_test_data()["base_url"]
    api_url = utils.get_test_data()["api_url"]

    try:
        page.goto(base_url)
        # Wait for network to be idle
        page.wait_for_load_state("networkidle")
    except Exception as e:
        logger.error(f"Failed to navigate to {base_url}: {e}")
        raise

    context = TestContext(page)

    yield context

    # TEARDOWN PHASE (Cleanup)
    logger.info(
        f"UI Test Teardown: "
        f"Starting cleanup for {len(context.created_booking_ids)} bookings"
    )
    token = utils.get_admin_auth_token()

    if token and context.created_booking_ids:
        headers = {
            "Content-Type": "application/json",
            "Cookie": f"token={token}",
            "User-Agent": "pytest"
        }
        for booking_id in context.created_booking_ids:
            try:
                response = requests.delete(
                    f"{api_url}/{booking_id}",
                    headers=headers,
                    timeout=10
                )
                if response.status_code in [201, 204, 200]:
                    logger.debug(f"Successfully deleted booking {booking_id}")
                else:
                    logger.warning(
                        f"Failed to delete booking {booking_id}."
                        f" Status: {response.status_code}"
                    )
            except Exception as e:
                logger.error(f"Error during cleanup of booking {booking_id}: {e}")

    logger.info("UI Test Teardown: Finished")
