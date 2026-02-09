# QA Automation Starter Kit

Professional test automation framework using Python + Playwright with modular architecture based on Page Object Model and modern best practices.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Architectural Pillars](#key-architectural-pillars)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Standard Practices](#standard-practices)
- [Fixtures & Test Utilities](#fixtures--test-utilities)
- [CI/CD Integration](#cicd-integration)

---

## Project Overview

Ready-to-use test automation starter kit for new projects. This framework demonstrates industry best practices with working examples using public test sites:

- **UI Tests**: SauceDemo (https://www.saucedemo.com) - E-commerce demo application
- **API Tests**: JSONPlaceholder (https://jsonplaceholder.typicode.com) - Free REST API for testing

**Main Goal**: Provide a professional, scalable foundation for test automation projects following senior-level standards.

---

## Key Architectural Pillars

### 1. Modular Page Object Model (POM)

All page objects inherit from `BasePage` to share common functionality and ensure consistency.

```python
class BasePage:
    def __init__(self, page: Page):
        self.page = page

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator("[data-test='username']")
```

**Encapsulated Components**: Each component has its own context (`self.root`) and all locators are scoped to avoid collisions.

```python
class ProductCard:
    def __init__(self, page: Page, root: Locator):
        self.page = page
        self.root = root
        self.name = self.root.locator(".inventory_item_name")  # Scoped
```

**Fluent Interface**: Methods return `self` or a new page instance to enable method chaining.

```python
def navigate(self, base_url: str) -> "LoginPage":
    self.page.goto(base_url)
    return self
```

---

### 2. Auth Reuse (Session Persistence)

**Pattern**: Authentication once per session using `authenticated_context` (session-scoped fixture).

```python
@pytest.fixture(scope="session")
def authenticated_context(playwright: Playwright, browser_type_launch_args) -> BrowserContext:
    """Perform login via UI once per session."""
    browser = playwright.chromium.launch(**browser_type_launch_args)
    context = browser.new_context()
    page = context.new_page()
    
    # UI login using LoginPage (fluent interface)
    login_page = LoginPage(page)
    login_page.navigate("https://www.saucedemo.com")
    login_page.login("standard_user", "secret_sauce")
    login_page.wait_for_successful_login()
    
    page.close()
    yield context
    
    context.close()
    browser.close()
```

**Advantages**:
- Performance: Login once per session (saves ~3-5s per test)
- Maintainability: Centralized logic in a single fixture
- Reusability: All tests share the same authenticated state

---

### 3. API Architecture with Pydantic

**Centralized API Management**: All APIs accessed through `APIManager` with automatic type validation using Pydantic.

```python
# Usage in tests
def test_get_user(api_client):
    # Act
    user_data = api_client.users.get_user(2)
    
    # Assert with Pydantic schema validation
    validated_user = UserResponse(**user_data)
    assert validated_user.id == 2
```

**Pydantic Schema Validation**:

```python
class UserResponse(BaseModel):
    """Schema for user data validation."""
    id: int = Field(..., description="User unique identifier")
    email: str = Field(..., description="User email address")
    first_name: str = Field(..., description="User first name")
    last_name: str = Field(..., description="User last name")
```

---

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.9+ | Base language |
| **Playwright** | 1.57.0 | Browser automation |
| **Pytest** | Latest | Testing framework |
| **Allure Reports** | Latest | Visual reports |
| **Pydantic** | 2.12+ | API schema validation |
| **Python Logging** | Built-in | Structured logging |

---

## Project Structure

```
.
├── apis/                           # API clients
│   ├── base_api.py                # Base class with auth and logging
│   ├── user_api.py                # User API (ReqRes.in example)
│   ├── api_manager.py             # Central API orchestrator
│   └── schemas/                   # Pydantic schemas
│       └── user_schemas.py
├── pages/                          # Page Objects
│   ├── base_page.py               # Base page with common methods
│   ├── login_page.py              # Login page (SauceDemo)
│   ├── inventory_page.py          # Inventory page (SauceDemo)
│   └── components/                # Reusable components
│       └── product_card.py
├── tests/                          # Test suite
│   ├── conftest.py                # Global fixtures
│   ├── api/                       # API contract tests
│   │   └── test_users.py
│   └── ui/                        # UI/E2E tests
│       ├── test_login.py
│       └── test_inventory.py
├── config/
│   └── settings.py                # Environment configuration
├── utils/
│   └── data_provider.py           # Test data helper
├── pytest.ini                      # Centralized pytest configuration
├── requirements.txt                # Python dependencies
└── README.md
```

---

## Getting Started

### Prerequisites

- **Python 3.9+**
- **Git**

### 1. Clone Repository

```bash
git clone <repository-url>
cd my-senior-start-kit
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Run Tests

```bash
# Run all tests
pytest

# Run specific module
pytest tests/ui/test_login.py

# Run API tests only
pytest tests/api/

# Run UI tests only
pytest tests/ui/

# Run with live logs
pytest --log-cli-level=INFO
```

### 5. View Reports

```bash
# HTML Report
open reports/report.html

# Allure Report (requires Allure CLI)
allure serve reports/allure-results
```

---

## Standard Practices

### Naming Conventions

| Element | Format | Examples |
|----------|---------|----------|
| **Classes** | PascalCase | `LoginPage`, `ProductCard` |
| **Methods** | `verb_noun` | `open_modal()`, `get_user()` |
| **Locators** | `description_type` | `save_button`, `username_input` |
| **Variables** | snake_case | `user_id`, `product_name` |
| **Constants** | UPPER_SNAKE_CASE | `EXPECTED_STATUS`, `BASE_URL` |

### AAA Test Pattern

All tests follow the Arrange-Act-Assert pattern:

```python
def test_add_product_to_cart(setup):
    # Arrange
    # - User is already logged in via session context.
    # - Declare product to add to cart.
    page = setup
    PRODUCT_NAME = "Sauce Labs Backpack"
    EXPECTED_CART_COUNT = 1
    
    # Act
    # - Navigate to inventory page and add product.
    inventory_page = InventoryPage(page)
    product = inventory_page.get_product_by_name(PRODUCT_NAME)
    product.add_to_cart()
    
    # Assert
    # - Validate cart badge shows correct count.
    expect(inventory_page.cart_badge).to_be_visible()
    expect(inventory_page.cart_badge).to_have_text(str(EXPECTED_CART_COUNT))
```

### Web-First Assertions

```python
# Good: Web-first assertions with auto-retry
expect(page.locator(".status")).to_be_visible()
expect(product.name).to_have_text("Backpack")

# Avoid: Python assert (no automatic retry)
assert page.locator(".status").is_visible()
```

### Professional Logging

```python
# Good: Structured logging
self.logger.info(f"User created: {name} (ID: {user_id})")
self.logger.debug(f"Creating user with name: {name}")
self.logger.error(f"Failed to create user: {error}")

# Avoid: print() statements
print("Creating user...")
```

---

## Fixtures & Test Utilities

### Core Fixtures (conftest.py)

| Fixture | Scope | Purpose | Returns |
|---------|-------|---------|---------|
| `authenticated_context` | session | Authenticated browser context (login 1x) | `BrowserContext` |
| `setup` | function | Authenticated page ready to use | `Page` |
| `setup_no_auth` | function | Unauthenticated page (public pages) | `Page` |
| `api_client` | function | API Manager for API tests | `APIManager` |
| `unique_name` | function | Unique timestamp for test names | `str` |

### Usage Examples

```python
def test_successful_login(setup_no_auth):
    """Test without authentication."""
    page = setup_no_auth
    login_page = LoginPage(page)
    login_page.navigate("https://www.saucedemo.com")
    # ... test logic

def test_add_to_cart(setup):
    """Test with authentication (already logged in)."""
    page = setup  # Already logged in via session context
    inventory_page = InventoryPage(page)
    # ... test logic

def test_create_user(api_client, unique_name):
    """API test with unique name."""
    user_name = f"test_user_{unique_name}"
    user_data = api_client.users.create_user(user_name, "QA Engineer")
    # ... test logic
```

---

## CI/CD Integration

### Execution Configuration

**All execution settings are centralized in `pytest.ini`**:

```ini
[pytest]
addopts = --browser chromium --html=reports/report.html --alluredir=reports/allure-results --tracing=retain-on-failure
```

**Why**: Single source of truth, consistency between local and CI/CD, simplified maintenance.

---

## Customizing for Your Project

### 1. Update Environment Configuration

Edit `config/settings.py` and create `.env` file:

```env
BASE_URL=https://your-app.com
USER_EMAIL=test@example.com
PASSWORD=your-password
```

### 2. Create Your Page Objects

```python
# pages/your_page.py
from pages.base_page import BasePage

class YourPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Add your locators
```

### 3. Create Your API Clients

```python
# apis/your_api.py
from apis.base_api import BaseAPI

class YourAPI(BaseAPI):
    def __init__(self, request_context):
        super().__init__(request_context)
        self.base_url = "https://your-api.com"
```

### 4. Update APIManager

```python
# apis/api_manager.py
class APIManager:
    def __init__(self, request_context):
        self.your_api = YourAPI(request_context)
```

### 5. Update conftest.py

Update `authenticated_context` fixture with your app's login logic.

---

## Additional Resources

- **ARCHITECTURE.md**: Detailed architecture documentation
- **STATE_OF_THE_ART.md**: Modern practices guide (Pydantic validation, Clean Architecture)
- **.cursorrules**: Complete code standards and best practices
- **Playwright Docs**: https://playwright.dev/python/
- **Pytest Docs**: https://docs.pytest.org/
- **Pydantic Docs**: https://docs.pydantic.dev/

---

## Contributing

When contributing code to this project, make sure to:

1. Follow naming conventions in `.cursorrules`
2. Implement type hints in all methods
3. Use AAA pattern in all tests
4. Scope locators to `self.root` in components
5. Use `expect()` for assertions (not `assert`)
6. Use logging (not `print()`)

---

**Maintainer**: QA Automation Team  
**Last Updated**: February 2026  
**Framework Version**: Starter Kit 1.0
