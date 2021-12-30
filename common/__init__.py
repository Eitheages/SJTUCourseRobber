class Course():
    """
    用课程类型、教学班ID代表唯一的一个课程
    """
    def __init__(self, id_: str, class_: str = "主修课程",) -> None:
        self.class_ = class_
        self.id_ = id_
    
    def __str__(self) -> str:
        return self.class_ + " " + self.id_
