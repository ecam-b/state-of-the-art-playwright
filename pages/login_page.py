from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    SauceDemo Login page - https://www.saucedemo.com
    Generic example for starter kit.
    """
    
    def __init__(self, page: Page):
        super().__init__(page)
        # Form inputs
        self.username_input = page.locator("[data-test='username']")
        self.password_input = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")
        
        # Error message
        self.error_message = page.locator("[data-test='error']")

    def navigate(self, base_url: str) -> "LoginPage":
        """
        Navigate to login page.
        Returns self for method chaining.
        """
        self.page.goto(base_url)
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        """
        Perform login with credentials.
        Returns self for method chaining.
        
        Args:
            username: Username (e.g., standard_user)
            password: Password (e.g., secret_sauce)
        """
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return self
    
    def wait_for_successful_login(self, timeout: int = 5000) -> None:
        """
        Wait for successful login by checking URL change.
        
        Args:
            timeout: Maximum wait time in milliseconds
        """
        expect(self.page).to_have_url("https://www.saucedemo.com/inventory.html", timeout=timeout)
    
    def get_error_message(self) -> str:
        """
        Get error message text when login fails.
        Returns error message string.
        """
        return self.error_message.text_content()
