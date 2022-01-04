class ClassFull(Exception):
    """When a course is full, raise it."""

class ProcessShutException(Exception):
    """When it is necessary to end up the script, raise it.
    This is the only exception that cannot be dealt in code!
    """
    pass

class TimeConflict(Exception):
    """When alert box show "所选教学班的上课时间与其他教学班有冲突！", raise it."""
    pass

class CourseConflict(Exception):
    """When alert box show "一门课程最多可选1个志愿！", raise it."""
    pass

class AlreadyChoose(Exception):
    """When alert box show "您确定要退掉该课程吗？", raise it."""
    pass

class NotChosen(Exception):
    """When you want to quit a course you have not choose, raise it."""
    pass