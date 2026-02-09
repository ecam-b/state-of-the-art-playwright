import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def test_successful_login(setup_no_auth):
    """
    Validate successful login flow with valid credentials.
    Tests user can access inventory after login.
    """
    # Arrange
    # - Navigate to SauceDemo login page.
    # - Declare valid test credentials.
    page = setup_no_auth
    BASE_URL = "https://www.saucedemo.com"
    USERNAME = "standard_user"
    PASSWORD = "secret_sauce"
    
    # Act
    # - Navigate to login page.
    login_page = LoginPage(page)
    login_page.navigate(BASE_URL)
    # - Enter credentials and submit.
    login_page.login(USERNAME, PASSWORD)
    
    # Assert
    # - Validate successful redirect to inventory page.
    login_page.wait_for_successful_login()
    # - Validate inventory page elements are visible.
    inventory_page = InventoryPage(page)
    expect(inventory_page.title).to_be_visible()
    expect(inventory_page.title).to_have_text("Products")


def test_login_with_invalid_credentials(setup_no_auth):
    """
    Validate login fails with invalid credentials.
    Tests error message is displayed correctly.
    """
    # Arrange
    # - Navigate to SauceDemo login page.
    # - Declare invalid test credentials.
    page = setup_no_auth
    BASE_URL = "https://www.saucedemo.com"
    INVALID_USERNAME = "invalid_user"
    INVALID_PASSWORD = "wrong_password"
    EXPECTED_ERROR = "Username and password do not match"
    
    # Act
    # - Navigate to login page.
    login_page = LoginPage(page)
    login_page.navigate(BASE_URL)
    # - Enter invalid credentials and submit.
    login_page.login(INVALID_USERNAME, INVALID_PASSWORD)
    
    # Assert
    # - Validate error message is displayed.
    expect(login_page.error_message).to_be_visible()
    # - Validate error message contains expected text.
    expect(login_page.error_message).to_contain_text(EXPECTED_ERROR)


def test_login_with_locked_user(setup_no_auth):
    """
    Validate login fails with locked out user.
    Tests specific error for locked accounts.
    """
    # Arrange
    # - Navigate to SauceDemo login page.
    # - Use locked_out_user credentials.
    page = setup_no_auth
    BASE_URL = "https://www.saucedemo.com"
    LOCKED_USERNAME = "locked_out_user"
    PASSWORD = "secret_sauce"
    EXPECTED_ERROR = "this user has been locked out"
    
    # Act
    # - Navigate to login page.
    login_page = LoginPage(page)
    login_page.navigate(BASE_URL)
    # - Enter locked user credentials and submit.
    login_page.login(LOCKED_USERNAME, PASSWORD)
    
    # Assert
    # - Validate error message is displayed.
    expect(login_page.error_message).to_be_visible()
    # - Validate error message contains locked out text.
    expect(login_page.error_message).to_contain_text(EXPECTED_ERROR)
