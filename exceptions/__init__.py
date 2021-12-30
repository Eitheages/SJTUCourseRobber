from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement

class ClassFull(Exception):
    """When a course is full, raise it."""

class ProcessWrongException(Exception):
    """When the script is working with wrong process, raise it."""
    pass

class ProcessShutException(Exception):
    """When it is necessary to end up the script, raise it."""
    pass

class TimeConflict(Exception):
    """When alert box show "所选教学班的上课时间与其他教学班有冲突！", raise it."""
    pass

class CourseConflict(Exception):
    """When alert box show "一门课程最多可选1个志愿！", raise it."""
    pass