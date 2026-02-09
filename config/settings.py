import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class Config:
    """
    Environment configuration from .env file.
    
    Note: This starter kit uses public APIs and test sites:
    - SauceDemo (UI): https://www.saucedemo.com
    - ReqRes.in (API): https://reqres.in
    
    For your own projects, configure these in .env file:
    - BASE_URL: Your application URL
    - USER_EMAIL: Test user email
    - PASSWORD: Test user password
    """
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    USER_EMAIL = os.getenv("USER_EMAIL", "standard_user")
    PASSWORD = os.getenv("PASSWORD", "secret_sauce")


# Validation and startup log
logger.info(f"Starting tests with BASE_URL: {Config.BASE_URL}")