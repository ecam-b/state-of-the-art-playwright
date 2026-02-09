from typing import Any
from apis.post_api import PostAPI


class APIManager:
    """
    Central API manager providing access to example APIs.
    
    This is a generic starter kit example using public APIs:
    - JSONPlaceholder for RESTful API examples
    
    Usage:
        api = APIManager(request_context)
        
        # Post API (JSONPlaceholder - no auth required)
        api.posts.get_post(1)
        api.posts.create_post("Title", "Body", 1)
    """
    
    def __init__(self, request_context: Any):
        """
        Initialize API Manager with request context.
        
        Args:
            request_context: Playwright request context from page.request
        """
        self._request_context = request_context
        self._token = None
        
        # Example APIs
        self.posts = PostAPI(request_context)
    
    def login(self, username: str = "", password: str = "", response_user: str = "true") -> str:
        """
        Login method for consistency with framework pattern.
        JSONPlaceholder doesn't require authentication, so this is a no-op.
        Returns mock token string.
        """
        # JSONPlaceholder doesn't require authentication
        self._token = "no-auth-required"
        self.posts.token = self._token
        
        return self._token
    
    @property
    def token(self) -> str:
        """Get current authentication token."""
        return self._token
