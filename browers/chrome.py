# -*- coding:utf-8 -*-
from selenium.common.exceptions import NoSuchElementException
from common.setup import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from exceptions import *
from . import nowtime
import time
from typing import List


class CourseRobber():
    """
    Add some specifical function, just for SJTU coures rob.
    """
    def __init__(self, capabilities: dict = None, account: str = "", password: str = "") -> None:
        self._brower = webdriver.Chrome(desired_capabilities = capabilities)
        self._diary = ""
        self._account = account
        self._password = password
        self.__file = open(r"./diary.txt", "a", encoding='utf-8')
        self.__file.write("\n\n{}启动CourseRobber\n".format(nowtime()))

    def __str__(self) -> str:
        return self._diary[:-1]

    def mark(self, info: str) -> None:
        """To print, save, and mark the information.
        Time and <br> default.
        """
        print(temp := "{}{}\n".format(nowtime(), info), end = "")
        self._diary += temp
        self.__file.write(temp)

    def enter(self, url: str) -> str:
        """
        Enter the website, return the title.
        """
        self._brower.get(url)
        title = self._brower.title
        self.mark("打开{}".format(title))
        return title

    def login(self, cookies: dict = None) -> None:
        """To login the https://i.sjtu.edu.cn"""

        if "上海交通大学教学信息服务网" not in self.enter(r"https://i.sjtu.edu.cn/"):
            self.mark("错误日志：未进入上海交通大学教学信息服务网")
            raise ProcessShutException
        if cookies is not None:
            for cookie in cookies:
                self._brower.add_cookie(cookie_dict=cookie)
            title =  self.enter(r"https://i.sjtu.edu.cn/")
            if "教学管理信息服务平台" in title:
                self.mark("Cookies验证通过！")
                return
            elif "上海交通大学教学信息服务网" in title:
                self.mark("提示：cookies已失效，尝试手动登录")
            else:
                self.mark("错误日志：未进入上海交通大学教学信息服务网")
                raise ProcessShutException
        try:
            # find the button of "Jaccount Login", click it.
            self._brower.find_element(By.XPATH, "//*[@id=\"authJwglxtLoginURL\"]").click()

            if "上海交通大学统一身份认证" not in self._brower.title:
                self.mark("错误日志：未进入Jaccount登陆界面")
                raise ProcessShutException
            else:
                self.mark("进入jaccount登陆界面")
            
            # put in account and password
            account_box = self._brower.find_element(By.XPATH, "//*[@id=\"user\"]")
            account_box.clear()
            account_box.send_keys(self._account)
            password_box = self._brower.find_element(By.XPATH, "//*[@id=\"pass\"]")
            password_box.clear()
            password_box.send_keys(self._password)
            self.mark("输入账号和密码")
            
            # Entering verification code, you have 20 seconds.
            WebDriverWait(self._brower, timeout=20).until(lambda d: d.title=="教学管理信息服务平台" and d.find_element(By.XPATH, "//*[@id=\"cdNav\"]"))
            self.mark("进入教学管理信息服务平台")

        except NoSuchElementException:
            self.mark("错误日志：因没有找到关键元素，程序终止")
            raise ProcessShutException

    def check_alert(self) -> None:
        """
        Check if there is an alert box.
        Do nothing when there is no; close it when there is.
        """
        try:
            alert_close = self._brower.find_element(By.XPATH, "//*[@id=\"alertModal\"]/div/div/div[1]/button")
            alert_close.click()
            raise ClassFullException
        except NoSuchElementException:
            pass

    def jump(self)->None:
        '''
        After approach "教学管理信息服务平台", jump to class-choosing page.
        '''
        if "教学管理信息服务平台" not in self._brower.title:
            self.mark("错误日志：未进入教学管理信息服务平台")
            raise ProcessShutException
        try:
            xuanke = self._brower.find_elements(By.XPATH, "//*[@id=\"drop1\"]")[2]
            xuanke.click()
            zizhuxuanke = self._brower.find_element(By.XPATH, "//*[@id=\"cdNav\"]/ul/li[3]/ul/li[3]/a")
            zizhuxuanke.click()

            # jump to the new page
            self._brower.switch_to.window(self._brower.window_handles[-1])
            WebDriverWait(self._brower,timeout=10).until(lambda d: d.title=="自主选课")
        except NoSuchElementException:
            self.mark("错误日志：因没有找到关键元素，程序终止")
            raise ProcessShutException

    def rob_course(self, keyword: str, class_: str = "主修课程", pause_time: ... = 0.3) -> str:
        '''
        Input what you want to search in the box, try to choose that.
        Remember to put in the type of course(default: "主修课程") that you want to choose simultaneously.
        Try to make sure the keyword refer to a single class.
        if there're no exceptions, 'button_list' will contain:
            主修课程
            民族生课程
            留学生及港澳台生
            板块课(大学英语)
            板块课(体育（2）)
            通识课
            新生研讨课
            通选课
            点此查看更多
        The last one is also important as it provides an opportunity to expand the incomplete list.
        '''
        if self._brower.title != "自主选课":
            self.mark("错误日志：未进入自主选课页面！")
            raise ProcessShutException
        try:
            button_list = self._brower.find_elements(By.XPATH, "//a[@href=\"javascript:void(0)\"]")
            for button in button_list:
                if class_ in button.text:
                    button.click()
                    break
            # This break is essentially important!!!(Don't ask how I know.)
            time.sleep(pause_time)
            input_box = WebDriverWait(self._brower, timeout=5, poll_frequency=0.1).until(
                lambda d: d.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/input")
            )
            input_box.clear()
            input_box.send_keys(keyword)
            chaxun = self._brower.find_element(By.XPATH, "//*[@id=\"searchBox\"]/div/div[1]/div/div/div/div/span/button[1]")
            chaxun.click()
            time.sleep(pause_time)
            waiting = self._brower.find_element(By.XPATH,"//tr[@class=\"body_tr\"]")
            waiting.find_element(By.TAG_NAME, "button").click()
            try:
                self.check_alert()
            except ClassFullException:
                return "课程人数已满，选课失败！"
            return "选课成功！"
        except NoSuchElementException:
            return "因为未找到关键元素，选课失败！"

    def rob_coures(self, courses: List[List[str]]) -> None:
        '''
        Input a dict include the courses, try to rob the course.
        courses list should be like this:[
            ["class_", "keyword",]
            ...
        ]where 'class_' means the type(no default), 'keyword' means the word you want to search.
        '''
        i = 1
        for course in courses:
            info = "第{}条课程:".format(i)
            i += 1
            try:
                info += self.rob_course(keyword=course[1], class_=course[0])
                self.mark(info)
            except ProcessShutException as e:
                raise e
        return info

    def quit(self) -> None:
        self._brower.quit()
        self.__file.close()
    
    def __del__(self) -> None:
        self.__file.close()