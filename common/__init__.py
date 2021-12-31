class Course():
    """
    用课程类型、教学班ID代表唯一的一个课程
    """
    def __init__(self, id_: str, class_: str = "主修课程",) -> None:
        self.class_ = class_
        self.id_ = id_
    
    def __str__(self) -> str:
        return self.class_ + " " + self.id_

class CourseInfo():
    """
    存储课程具体信息
    包含课程号、课程名、教师、上课时间、已选人数/人数上限、选课按钮(网页元素)
    分别对应："id", "name", "teacher", "class_time", "status", "button"
    或者用0-5索引访问
    """
    def __init__(self, id_: str):
        self._content = {"id": id_}
