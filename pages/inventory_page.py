from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from pages.components.product_card import ProductCard


class InventoryPage(BasePage):
    """
    SauceDemo Inventory page - https://www.saucedemo.com/inventory.html
    Generic example for starter kit.
    """
    
    def __init__(self, page: Page):
        super().__init__(page)
        # Page title
        self.title = page.locator(".title")
        
        # Product sort dropdown
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        
        # Product items container
        self.products_container = page.locator(".inventory_list")
        
        # Shopping cart
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        
        # Burger menu
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")
    
    def get_product_cards(self) -> list[ProductCard]:
        """
        Get all product cards on the page.
        Returns list of ProductCard objects.
        """
        items = self.products_container.locator(".inventory_item").all()
        return [ProductCard(self.page, item) for item in items]
    
    def get_product_by_name(self, product_name: str) -> ProductCard:
        """
        Get product card by product name.
        Returns ProductCard object.
        """
        product_locator = self.products_container.locator(".inventory_item", has_text=product_name)
        return ProductCard(self.page, product_locator)
    
    def sort_products(self, sort_option: str) -> "InventoryPage":
        """
        Sort products by option.
        Returns self for method chaining.
        
        Args:
            sort_option: Sort option (az, za, lohi, hilo)
        """
        self.sort_dropdown.select_option(sort_option)
        return self
    
    def get_cart_count(self) -> int:
        """
        Get number of items in cart from badge.
        Returns count as integer, or 0 if badge not visible.
        """
        if self.cart_badge.is_visible():
            return int(self.cart_badge.text_content())
        return 0
    
    def open_cart(self) -> None:
        """Navigate to shopping cart page."""
        self.cart_link.click()
    
    def logout(self) -> None:
        """Logout from application."""
        self.menu_button.click()
        self.logout_link.click()
