import pytest
from playwright.sync_api import expect
from pages.inventory_page import InventoryPage


def test_add_product_to_cart(setup):
    """
    Validate user can add product to shopping cart.
    Tests cart badge updates correctly.
    """
    # Arrange
    # - User is already logged in via session context.
    # - Declare product to add to cart.
    page = setup
    PRODUCT_NAME = "Sauce Labs Backpack"
    EXPECTED_CART_COUNT = 1
    
    # Act
    # - Navigate to inventory page.
    inventory_page = InventoryPage(page)
    # - Add product to cart.
    product = inventory_page.get_product_by_name(PRODUCT_NAME)
    product.add_to_cart()
    
    # Assert
    # - Validate cart badge shows correct count.
    expect(inventory_page.cart_badge).to_be_visible()
    expect(inventory_page.cart_badge).to_have_text(str(EXPECTED_CART_COUNT))
    # - Validate product shows Remove button.
    expect(product.remove_button).to_be_visible()


def test_remove_product_from_cart(setup):
    """
    Validate user can remove product from shopping cart.
    Tests cart badge updates after removal.
    """
    # Arrange
    # - User is already logged in via session context.
    # - Add product to cart first.
    page = setup
    inventory_page = InventoryPage(page)
    PRODUCT_NAME = "Sauce Labs Bike Light"
    
    product = inventory_page.get_product_by_name(PRODUCT_NAME)
    product.add_to_cart()
    
    # Act
    # - Remove product from cart.
    product.remove_from_cart()
    
    # Assert
    # - Validate cart badge is not visible (empty cart).
    expect(inventory_page.cart_badge).not_to_be_visible()
    # - Validate product shows Add to Cart button.
    expect(product.add_to_cart_button).to_be_visible()


def test_product_price_display(setup):
    """
    Validate all products display valid prices.
    Tests price format and data integrity.
    """
    # Arrange
    # - User is already logged in via session context.
    page = setup
    inventory_page = InventoryPage(page)
    
    # Act
    # - Get all product cards from inventory.
    products = inventory_page.get_product_cards()
    
    # Assert
    # - Validate at least one product exists.
    assert len(products) > 0, "Inventory should contain products"
    
    # - Validate each product has valid price.
    for product in products:
        price = product.get_price()
        assert price > 0, f"Product {product.get_name()} should have positive price"
        assert isinstance(price, float), f"Price should be float, got {type(price)}"


def test_sort_products_by_price_low_to_high(setup):
    """
    Validate products can be sorted by price (low to high).
    Tests sorting functionality works correctly.
    """
    # Arrange
    # - User is already logged in via session context.
    page = setup
    inventory_page = InventoryPage(page)
    
    # Act
    # - Sort products by price (low to high).
    inventory_page.sort_products("lohi")
    
    # Assert
    # - Get all products after sorting.
    products = inventory_page.get_product_cards()
    prices = [product.get_price() for product in products]
    
    # - Validate prices are in ascending order.
    assert prices == sorted(prices), "Products should be sorted by price (low to high)"


def test_add_multiple_products_to_cart(setup):
    """
    Validate user can add multiple products to cart.
    Tests cart count updates correctly with multiple items.
    """
    # Arrange
    # - User is already logged in via session context.
    page = setup
    inventory_page = InventoryPage(page)
    PRODUCTS_TO_ADD = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
    EXPECTED_CART_COUNT = len(PRODUCTS_TO_ADD)
    
    # Act
    # - Add multiple products to cart.
    for product_name in PRODUCTS_TO_ADD:
        product = inventory_page.get_product_by_name(product_name)
        product.add_to_cart()
    
    # Assert
    # - Validate cart badge shows correct total count.
    expect(inventory_page.cart_badge).to_be_visible()
    expect(inventory_page.cart_badge).to_have_text(str(EXPECTED_CART_COUNT))
