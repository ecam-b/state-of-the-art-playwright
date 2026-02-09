from playwright.sync_api import Page, Locator


class ProductCard:
    """
    Product card component on SauceDemo inventory page.
    Encapsulates product information and actions.
    """
    
    def __init__(self, page: Page, root: Locator):
        """
        Initialize product card component.
        
        Args:
            page: Playwright page object
            root: Root locator for this product card
        """
        self.page = page
        self.root = root
        
        # Product elements (scoped to root)
        self.name = self.root.locator(".inventory_item_name")
        self.description = self.root.locator(".inventory_item_desc")
        self.price = self.root.locator(".inventory_item_price")
        self.image = self.root.locator(".inventory_item_img img")
        self.add_to_cart_button = self.root.locator("button[id^='add-to-cart']")
        self.remove_button = self.root.locator("button[id^='remove']")
    
    def get_name(self) -> str:
        """Get product name."""
        return self.name.text_content()
    
    def get_price(self) -> float:
        """
        Get product price as float.
        Removes $ symbol and converts to float.
        """
        price_text = self.price.text_content()
        return float(price_text.replace("$", ""))
    
    def get_description(self) -> str:
        """Get product description."""
        return self.description.text_content()
    
    def add_to_cart(self) -> "ProductCard":
        """
        Add product to cart.
        Returns self for method chaining.
        """
        self.add_to_cart_button.click()
        return self
    
    def remove_from_cart(self) -> "ProductCard":
        """
        Remove product from cart.
        Returns self for method chaining.
        """
        self.remove_button.click()
        return self
    
    def is_in_cart(self) -> bool:
        """
        Check if product is already in cart.
        Returns True if Remove button is visible.
        """
        try:
            return self.remove_button.is_visible(timeout=1000)
        except Exception:
            return False
    
    def click_name(self) -> None:
        """Click product name to view details."""
        self.name.click()
