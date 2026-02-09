import logging
from typing import Dict, Any


class BaseAPI:
    """Base API class with authentication, logging, and common HTTP operations."""
    
    def __init__(self, request_context: Any):
        self.request = request_context
        self.base_url = "https://api.example.com"  # Override in subclasses
        self.token = None
        
        # Initialize logger for this API instance
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def login(self, username: str, password: str, response_user: str = "true") -> str:
        """
        Perform login and store authentication token internally.
        Returns authentication token string.
        """
        self.logger.info(f"Attempting login for user: {username}")
        
        payload = {
            "username": username,
            "password": password,
            "response_user": response_user
        }
        
        response = self.request.post(f"{self.base_url}/api/v1/login/", data=payload)
        
        if not response.ok:
            self.logger.error(f"Login failed: {response.status} - {response.text()}")
            assert False, f"Login error: {response.text()}"
        
        self.token = f"Token {response.json()['token']}"
        self.logger.info(f"Login successful for user: {username}")
        
        return self.token

    def _get_headers(self) -> Dict[str, str]:
        """
        Get authorization headers for authenticated requests.
        Raises ValueError if not logged in.
        """
        if not self.token:
            self.logger.error("Attempted to make authenticated request without login")
            raise ValueError("Must login first using api.login()")
        return {"Authorization": self.token}
    
    def _log_request(self, method: str, url: str, status: int) -> None:
        """
        Log API request details.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            url: Request URL
            status: Response status code
        """
        if status >= 200 and status < 300:
            self.logger.info(f"{method} {url} - Status: {status}")
        elif status >= 400:
            self.logger.error(f"{method} {url} - Status: {status}")
        else:
            self.logger.warning(f"{method} {url} - Status: {status}")