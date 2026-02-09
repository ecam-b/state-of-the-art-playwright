from playwright.sync_api import Page, Locator


class BasePage:
    """Base page class with common functionality for all page objects."""
    
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str) -> None:
        """Navigate to specified URL."""
        self.page.goto(url)

    def click_until_visible(self, locator_to_click: Locator, locator_to_wait: Locator, max_retries: int = 3, timeout: int = 2000) -> None:
        """
        Click element and retry until target element becomes visible.
        Useful for handling timing issues with dynamic elements.
        """
        for _ in range(max_retries):
            try:
                locator_to_click.click()
                locator_to_wait.wait_for(state="visible", timeout=timeout)
                return
            except Exception:
                continue
        # Final attempt - let it fail with proper error if needed
        locator_to_click.click()
        locator_to_wait.wait_for(state="visible", timeout=timeout)
