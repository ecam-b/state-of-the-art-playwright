import logging
from datetime import datetime
from typing import Generator
import pytest
from playwright.sync_api import Page, BrowserContext, Playwright
from pages.login_page import LoginPage
from apis.api_manager import APIManager

# Configure logging for Allure reports
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def authenticated_context(playwright: Playwright, browser_type_launch_args: dict) -> Generator[BrowserContext, None, None]:
    """
    Create authenticated browser context once per session via UI login.
    Uses SauceDemo as example application.
    """
    browser = playwright.chromium.launch(**browser_type_launch_args)
    context = browser.new_context()
    page = context.new_page()
    
    # Perform UI login using LoginPage (fluent interface)
    BASE_URL = "https://www.saucedemo.com"
    USERNAME = "standard_user"
    PASSWORD = "secret_sauce"
    
    login_page = LoginPage(page)
    login_page.navigate(BASE_URL).login(USERNAME, PASSWORD)
    login_page.wait_for_successful_login()
    
    logger.info("Session authentication completed successfully")
    
    page.close()
    
    yield context
    
    context.close()
    browser.close()


@pytest.fixture(scope="function")
def setup(authenticated_context: BrowserContext) -> Generator[Page, None, None]:
    """
    Setup authenticated page using session context.
    Creates new page with auth state already active.
    """
    page = authenticated_context.new_page()
    page.goto("https://www.saucedemo.com/inventory.html")
    
    yield page
    
    page.close()


@pytest.fixture(scope="function")
def setup_no_auth(page: Page) -> Generator[Page, None, None]:
    """
    Setup unauthenticated page for public pages.
    Configures viewport without login flow.
    """
    page.set_viewport_size({"width": 1920, "height": 1080})
    yield page


@pytest.fixture
def unique_name() -> Generator[str, None, None]:
    """
    Generate unique timestamp-based name for test data.
    Returns string in format: HH_MM_YYYY_MM_DD.
    """
    timestamp = datetime.now().strftime("%H_%M_%Y_%m_%d")
    yield timestamp


@pytest.fixture(scope="function")
def api_client(playwright: Playwright) -> Generator[APIManager, None, None]:
    """
    Central API Manager for pure API tests (no browser needed).
    
    Usage in API tests (tests/api/):
        # Example: ReqRes.in API
        api_client.users.get_user(1)
        api_client.users.create_user("John", "Developer")
    
    Note: ReqRes.in doesn't require authentication.
    """
    # Create standalone request context for API-only tests
    request_context = playwright.request.new_context()
    
    api_manager = APIManager(request_context)
    api_manager.login()  # No-op for ReqRes.in
    
    yield api_manager
    
    # Cleanup request context
    request_context.dispose()
