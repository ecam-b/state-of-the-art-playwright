# Framework Architecture

This document describes the architectural organization of the test automation starter kit.

---

## Architecture Overview

The framework follows a clear separation between **Business APIs** (application management) and **UI Layer** (page objects), with a centralized access point through `APIManager`.

```
┌─────────────────────────────────────────────────────────────┐
│                        APIManager                            │
│  (Central fixture: api_client)                              │
├──────────────────────────────────────────────────────────────┤
│                    Example APIs                             │
│           (JSONPlaceholder - Public API)                    │
├──────────────────────────────────────────────────────────────┤
│  • api_client.posts                                         │
│                                                             │
│  Methods:                                                   │
│  - get_post(id)                                            │
│  - get_posts(user_id)                                      │
│  - create_post(title, body, user_id)                       │
│  - update_post(id, title, body, user_id)                   │
│  - delete_post(id)                                         │
└──────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
.
├── apis/                              # API Layer
│   ├── api_manager.py                 # Central API Manager
│   ├── base_api.py                    # Base class with auth and logging
│   ├── post_api.py                    # Example: Post API (JSONPlaceholder)
│   └── schemas/                       # Pydantic schemas
│       └── post_schemas.py            # Post API schemas
│
├── pages/                             # UI Layer
│   ├── base_page.py                   # Base page with common methods
│   ├── login_page.py                  # Login page (SauceDemo)
│   ├── inventory_page.py              # Inventory page (SauceDemo)
│   └── components/                    # Reusable components
│       └── product_card.py            # Product card component
│
├── tests/
│   ├── conftest.py                    # Global fixtures
│   ├── ui/                            # UI/E2E Tests
│   │   ├── test_login.py
│   │   └── test_inventory.py
│   └── api/                           # API Contract Tests
│       └── test_posts.py
```

---

## Key Concepts

### 1. APIManager (api_client fixture)

Central object providing unified access to all APIs with shared authentication.

```python
# In conftest.py
@pytest.fixture
def api_client(playwright: Playwright) -> APIManager:
    """Central API Manager with shared session."""
    request_context = playwright.request.new_context()
    api_manager = APIManager(request_context)
    api_manager.login()  # Handle auth centrally
    return api_manager
```

### 2. Business APIs

**Purpose**: Manage application via API (equivalent to Postman collection)

**Usage in tests**:
```python
def test_get_user(api_client):
    # Business API for application management
    user_data = api_client.users.get_user(2)
    
    # Validate with Pydantic
    validated_user = UserResponse(**user_data)
    assert validated_user.id == 2
```

**Available APIs**:
- `api_client.posts` → PostAPI (get, create, update, delete posts)

### 3. BaseAPI Pattern

All API clients inherit from `BaseAPI` to share common functionality:

```python
class BaseAPI:
    def __init__(self, request_context):
        self.request = request_context
        self.base_url = "https://api.example.com"
        self.token = None
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def login(self, username: str, password: str) -> str:
        """Perform login and store token."""
        # Implementation
        pass
    
    def _get_headers(self) -> Dict[str, str]:
        """Get auth headers for requests."""
        return {"Authorization": self.token}
    
    def _log_request(self, method: str, url: str, status: int) -> None:
        """Log API request with appropriate level."""
        # Implementation
        pass
```

---

## Test Organization

### tests/ui/ - UI/E2E Tests

**Purpose**: Validate user workflows through the UI

**Characteristics**:
- Use Page Objects for UI interactions
- Use `setup` fixture for authenticated pages
- Use `setup_no_auth` for public pages (login)
- Focus on end-user scenarios

**Example**:
```python
def test_add_product_to_cart(setup):
    # Arrange
    page = setup  # Already logged in
    PRODUCT_NAME = "Sauce Labs Backpack"
    
    # Act - UI interaction
    inventory_page = InventoryPage(page)
    product = inventory_page.get_product_by_name(PRODUCT_NAME)
    product.add_to_cart()
    
    # Assert - UI validation
    expect(inventory_page.cart_badge).to_be_visible()
```

### tests/api/ - API Contract Tests

**Purpose**: Validate API contracts and server logic

**Characteristics**:
- Direct API calls (no UI)
- Validate response structure with Pydantic
- Test business logic at API level
- Equivalent to Postman requests

**Example**:
```python
def test_get_user_contract(api_client):
    # Arrange
    user_id = 2
    
    # Act - Direct API call
    user_data = api_client.users.get_user(user_id)
    
    # Assert - Pydantic contract validation
    validated_user = UserResponse(**user_data)
    assert validated_user.id == user_id
    assert "@" in validated_user.email
```

---

## Pydantic Schema Validation

### Why Pydantic?

**Before (Manual Validation)**:
```python
# Error-prone, repetitive
assert "id" in response
assert isinstance(response["id"], int)
assert "email" in response
assert isinstance(response["email"], str)
# ... 20+ more checks
```

**After (Pydantic)**:
```python
# Automatic, complete validation
validated_user = UserResponse(**response)
# All fields validated automatically!
```

### Schema Definition

```python
from pydantic import BaseModel, Field

class UserResponse(BaseModel):
    """Schema for user data validation."""
    
    id: int = Field(..., description="User unique identifier")
    email: str = Field(..., description="User email address")
    first_name: str = Field(..., description="User first name")
    last_name: str = Field(..., description="User last name")
    avatar: str = Field(..., description="User avatar URL")
```

### Benefits

- Automatic type checking
- Self-documenting API contracts
- IDE auto-completion
- Fails fast on schema changes
- Maintainable (change schema once, all tests benefit)

---

## Authentication & Token Sharing

### Session Authentication

For UI tests, authentication happens once per session using `authenticated_context` fixture.

```python
@pytest.fixture(scope="session")
def authenticated_context(playwright, browser_type_launch_args):
    """Login once per session, reuse context."""
    browser = playwright.chromium.launch(**browser_type_launch_args)
    context = browser.new_context()
    page = context.new_page()
    
    # UI login using LoginPage
    login_page = LoginPage(page)
    login_page.navigate("https://www.saucedemo.com")
    login_page.login("standard_user", "secret_sauce")
    login_page.wait_for_successful_login()
    
    page.close()
    yield context
    
    context.close()
    browser.close()
```

**Benefits**:
- Login once per session (performance)
- Consistent auth across all UI tests
- No auth management in individual tests

### API Authentication

For API tests, authentication is handled by `APIManager`.

```python
class APIManager:
    def login(self, username: str = "", password: str = "") -> str:
        """Handle authentication centrally."""
        # In ReqRes.in example, no auth required
        self._token = "no-auth-required"
        self.users.token = self._token
        return self._token
```

---

## Usage Examples

### UI Test Example

```python
def test_successful_login(setup_no_auth):
    # Arrange
    page = setup_no_auth
    BASE_URL = "https://www.saucedemo.com"
    USERNAME = "standard_user"
    PASSWORD = "secret_sauce"
    
    # Act - UI interaction
    login_page = LoginPage(page)
    login_page.navigate(BASE_URL)
    login_page.login(USERNAME, PASSWORD)
    
    # Assert - UI validation
    login_page.wait_for_successful_login()
    inventory_page = InventoryPage(page)
    expect(inventory_page.title).to_be_visible()
```

### API Contract Test Example

```python
def test_get_users_list(api_client):
    # Arrange
    page_number = 2
    
    # Act - API call
    response_data = api_client.users.get_users(page=page_number)
    
    # Assert - Pydantic validation
    validated_response = UserListResponse(**response_data)
    assert validated_response.page == page_number
    assert len(validated_response.data) > 0
```

---

## Adding New APIs

### 1. Create API Client

```python
# apis/product_api.py
from apis.base_api import BaseAPI

class ProductAPI(BaseAPI):
    def __init__(self, request_context):
        super().__init__(request_context)
        self.base_url = "https://your-api.com"
    
    def get_product(self, product_id: int) -> Dict[str, Any]:
        """Get product by ID."""
        response = self.request.get(f"{self.base_url}/products/{product_id}")
        self._log_request("GET", f"/products/{product_id}", response.status)
        return response.json()
```

### 2. Create Pydantic Schema

```python
# apis/schemas/product_schemas.py
from pydantic import BaseModel, Field

class ProductResponse(BaseModel):
    """Schema for product data validation."""
    id: int = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price")
```

### 3. Register in APIManager

```python
# apis/api_manager.py
class APIManager:
    def __init__(self, request_context):
        self.users = UserAPI(request_context)
        self.products = ProductAPI(request_context)  # Add new API
    
    def login(self, username: str = "", password: str = "") -> str:
        # Share token with all APIs
        self.users.token = self._token
        self.products.token = self._token
```

### 4. Use in Tests

```python
def test_get_product(api_client):
    product_data = api_client.products.get_product(1)
    validated_product = ProductResponse(**product_data)
    assert validated_product.price > 0
```

---

## Benefits of This Architecture

1. **Clear Separation**: APIs vs UI Layer
2. **Centralized Access**: Single `api_client` fixture
3. **Type Safety**: Pydantic validation for all APIs
4. **Professional Logging**: Structured logs with levels
5. **Scalability**: Easy to add new APIs and schemas
6. **Maintainability**: Changes isolated to specific files
7. **Performance**: Shared authentication reduces overhead

---

**Last Updated**: February 2026  
**Framework Version**: Starter Kit 1.0
