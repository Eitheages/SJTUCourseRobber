### 更新日志

+ 2021/12/29 重构了代码模块，代码整体更加有效和易读。考虑有空把所有的英文注释换成中文（三流英语还拿出来秀，明明只有中国人会用这个脚本！）
+ 2021/12/30 优化了代码结构，增添了alert检索，增添了一些高级操作（暂时没有写进主函数）。
+ 2021/12/31 重构了`rob_course`、`rob_courses`方法


### 待优化

+ 完善`CourseInfo`类并投入应用
+ 退课功能
+ 持续捡漏功能
+ 换课功能
+ 更多稳定性，可移植性
+ ……（有空慢慢写）

### 使用说明

+ （简单地说明关键操作。如果真的想深究，欢迎咨询本人，邮箱eitheage725@sjtu.edu.cn，或者自己看源代码。）

+ 目前只支持chrome浏览器，还需要安装对应的webdriver（自行百度？）

+ 创建一个packs文件夹，在里面新建secret.py文件，并写入：

    ```python
    class My():
        '''
        My account and password.
        Cookies included.
        '''
        account = "你的jaccount账号"
        password = "你的密码"
        cookies = [
            # 可以写cookies = None，则需要手动登录
            {'name': '_ga', 'value': 'GA1...'}, #一般不变
            {'name': 'kc@i.sjtu.edu.cn', 'value': 'ffff...'}, # 一般不变
            {'name': 'JSESSIONID', 'value': 'CF837...'}, # 会变
        ]
    
    class Courses():
        rob_list = [
            """写入你想要选的课程。格式如下："""
            # Course("(2021-2022-2)-AI002-1", "通选课")
            # Course("(2021-2022-2)-PHY1251-11") # 默认为主修课程
        ]
    ```
    
    安装对应的库（主要是selenium），运行main.py。尽情享受吧！