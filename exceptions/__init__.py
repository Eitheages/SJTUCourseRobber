from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement

class ClassFullException(WebDriverException):
    """When a course is full, raise it."""

class ProcessWrongException(Exception):
    """When the script is working with wrong process, raise it."""
    pass

class ProcessShutException(Exception):
    """When it is necessary to end up the script, raise it."""
    pass