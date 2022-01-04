# -*- coding:utf-8 -*-
import time
from . import nowtime
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import selenium.webdriver.support.expected_conditions as EC
from common import Course
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from exceptions import *
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

    def cat(self, info: str) -> None:
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
        self.cat("打开{}".format(title))
        return title

    def login(self, cookies: dict = None) -> None:
        """To login the https://i.sjtu.edu.cn"""

        if "上海交通大学教学信息服务网" not in self.enter(r"https://i.sjtu.edu.cn/"):
            self.cat("错误日志：未进入上海交通大学教学信息服务网")
            raise ProcessShutException
        self._brower.maximize_window()
        if cookies is not None:
            for cookie in cookies:
                self._brower.add_cookie(cookie_dict=cookie)
            title =  self.enter(r"https://i.sjtu.edu.cn/")
            if "教学管理信息服务平台" in title:
                self.cat("Cookies验证通过！")
                return
            elif "上海交通大学教学信息服务网" in title:
                self.cat("提示：cookies已失效，尝试手动登录")
            else:
                self.cat("错误日志：未进入上海交通大学教学信息服务网")
                raise ProcessShutException
        try:
            # find the button of "Jaccount Login", click it.
            self._brower.find_element(By.XPATH, "//*[@id=\"authJwglxtLoginURL\"]").click()

            if "上海交通大学统一身份认证" not in self._brower.title:
                self.cat("错误日志：未进入Jaccount登陆界面")
                raise ProcessShutException
            else:
                self.cat("进入jaccount登陆界面")
            
            # put in account and password
            account_box = self._brower.find_element(By.XPATH, "//*[@id=\"user\"]")
            account_box.clear()
            account_box.send_keys(self._account)
            password_box = self._brower.find_element(By.XPATH, "//*[@id=\"pass\"]")
            password_box.clear()
            password_box.send_keys(self._password)
            self.cat("输入账号和密码")
            
            # Entering verification code, you have 20 seconds.
            WebDriverWait(self._brower, timeout=20).until(lambda d: d.title=="教学管理信息服务平台" and d.find_element(By.XPATH, "//*[@id=\"cdNav\"]"))
            self.cat("进入教学管理信息服务平台")

        except NoSuchElementException:
            self.cat("错误日志：因没有找到关键元素，程序终止")
            raise ProcessShutException

    def jump(self)->None:
        '''
        After approach "教学管理信息服务平台", jump to class-choosing page.
        '''
        if "教学管理信息服务平台" not in self._brower.title:
            self.cat("错误日志：未进入教学管理信息服务平台！")
            raise ProcessShutException
        try:
            xuanke = self._brower.find_elements(By.XPATH, "//*[@id=\"drop1\"]")[2]
            xuanke.click()
            zizhuxuanke = self._brower.find_element(By.XPATH, "//*[@id=\"cdNav\"]/ul/li[3]/ul/li[3]/a")
            zizhuxuanke.click()

            # jump to the new page
            self._brower.switch_to.window(self._brower.window_handles[-1])
            WebDriverWait(self._brower,timeout=10).until(EC.title_is("自主选课"))
            self.cat("进入自主选课界面")
        except NoSuchElementException:
            self.cat("错误日志：因没有找到关键元素，程序终止")
            raise ProcessShutException

    def _pull(self) -> None:
        """
        Click 'down' button if it exits.
        """

        try:
            self._brower.find_element(By.XPATH, "//*[@class=\"down\"]").click()
        except NoSuchElementException:
            pass

    def _find_choices(self) -> dict:
        """
        Find the choice, make it a dict.
        """
        self._pull()
        choices = self._brower.find_elements(By.XPATH, "//a[@href=\"javascript:void(0);\"]")[:51]
        text = list(map(lambda e: e.text, choices))
        rdict = {text[i]: choices[i] for i in range(len(text))}
        return rdict

    def _find_classes(self) -> dict:
        """
        Find classes, make it a dict.
        """
        classes = self._brower.find_elements(By.XPATH, "//a[@href=\"javascript:void(0)\"]")
        text = list(map(lambda e: e.text, classes))
        rdict = {text[i]: classes[i] for i in range(len(text))}
        return rdict
        
    def _boom(self) -> dict:
        """
        Destruct the "自主选课" page, find elements that useful, except for choices.
        return a dict containing every useful elements.
        """
        chaxun_button = self._brower.find_element(By.XPATH, "//*[@id=\"searchBox\"]/div/div[1]/div/div/div/div/span/button[1]")
        chongzhi_button = self._brower.find_element(By.XPATH, "//*[@id=\"searchBox\"]/div/div[1]/div/div/div/div/span/button[2]")
        input_box = self._brower.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/input")
        rdict = {
            "click1": chaxun_button,
            "click2": chongzhi_button,
            "input": input_box,
        }
        return rdict

    def locate(self, course: Course, message = True) -> dict:
        """
        Locate the certain course by searching.
        Including exception check: title_is
        """
        # Considering whether to delete this exception check
        if self._brower.title != "自主选课":
            self.cat("错误日志：未进入自主选课页面！")
            raise ProcessShutException
        e_dict = self._boom()
        chaxun_button = e_dict["click1"]
        input_box = e_dict["input"]
        input_box.clear()
        input_box.send_keys(course.id_)
        chaxun_button.click()
        try:
            self._find_classes()[course.class_].click()
        except KeyError:
            self.cat("错误日志：无法找到对应课程类别，请检查是否输入有误！")
            raise ProcessShutException
        try:
            WebDriverWait(self._brower, timeout=20).until(lambda d: d.find_element(By.XPATH, "//*[@class=\"expand_close close1\"]"))
        except TimeoutException:
            self.cat("错误日志：无法根据课程号找到对应课程，请检查是否输入有误！")
            raise ProcessShutException
        rele: WebElement = self._brower.find_element(By.XPATH,"//*[@id=\"contentBox\"]/div[2]/div[1]")
        name = rele.find_element(By.XPATH, ".//h3[@class=\"panel-title\"]").find_element(By.XPATH, ".//a[@href=\"javascript:void(0);\"]").get_attribute('textContent')
        teacher = rele.find_element(By.XPATH, ".//td[@class= \"jsxmzc\"]").find_element(By.XPATH, ".//a[@href=\"javascript:void(0);\"]").get_attribute('textContent')
        class_time = rele.find_element(By.XPATH, ".//td[@class= \"sksj\"]").text.replace('\n', ' ')
        status = '/'.join(list(map(lambda e: e.get_attribute('textContent'), rele.find_element(By.XPATH, ".//td[@class= \"rsxx\"]").find_elements(By.XPATH, ".//font"))))
        button = rele.find_element(By.TAG_NAME, "button")
        rdict = {
            "name": name,
            "teacher": teacher,
            "class_time": class_time,
            "status": status,
            "button": button,
        }
        if message:
            self.cat("定位到课程{id}：{name} {teacher} {class_time} {status}".format(id=course.id_, name = name, teacher = teacher, class_time = class_time, status = status))
        return rdict

    def _check(self, info: dict):
        if info["status"].split('/')[0] == info["status"].split('/')[1]:
            raise ClassFull
        info["button"].click()
        try:
            alert_box: WebElement = self._brower.find_element(By.XPATH, "//*[@class=\"modal-content\"]")
            alert_info: str = alert_box.find_element(By.XPATH, ".//p").text
            alert_close = alert_box.find_element(By.XPATH, ".//button")
            alert_close.click()
            if "冲突" in alert_info:
                raise TimeConflict
            elif "志愿" in alert_info:  
                raise CourseConflict
            elif "退掉" in alert_info:
                raise AlreadyChoose
            else:
                # Normally, this line is not necessary.s
                raise ClassFull
        except NoSuchElementException:
            """no alert, rob successfully."""
            pass

    def _cancel(self, course: Course):
        info = self.locate(course)
        if info["button"].get_attribute("textContent") == "选课":
            self.cat("无法退课：未选上该课程！")
            raise NotChosen
        elif info["button"].get_attribute("textContent") == "退选":
            info["button"].click()
        try:
            alert_box: WebElement = self._brower.find_element(By.XPATH, "//*[@class=\"modal-content\"]")
            alert_close: list = alert_box.find_elements(By.XPATH, ".//button")
            alert_close[1].click()
            self.cat("退课成功！")
        except NoSuchElementException:
            self.cat("错误日志：意外错误！")
            raise ProcessShutException

    def rob_course(self, course: Course) -> None:
        """Try to rob course."""

        try:
            self._check(self.locate(course))
            self.cat("选课成功！")
        except ClassFull:
            self.cat("选课失败：人数已满！")
        except CourseConflict:
            self.cat("选课失败：志愿冲突！")
        except TimeConflict:
            self.cat("选课失败：时间冲突！")
        except AlreadyChoose:
            self.cat("选课失败：已经选择！")


    def rob_courses(self, courses: List[Course]) -> None:
        for course in courses:
            self.rob_course(course)

    def change_courses(self, course_desired: Course, courses_cancel: List[Course] = None) -> None:
        """
        Cancel a series of course, then try to choose the course.
        Before choose, firstly check if the course is full.

        !!Attention: The action is extremely dangerous, as you may lose many courses
        and receive a failure while robbing the desired courese.
        """
        if courses_cancel is not None:
            coure_desired_status = self.locate(course_desired)["status"]
            if coure_desired_status.split('/')[0] == coure_desired_status.split('/')[1]:
                self.cat("选课失败：人数已满！")
                return
            for course in courses_cancel:
                try:
                    self._cancel(course)
                except NotChosen:
                    continue
        self.rob_course(course_desired)
        
    def pick(self, course, pause_time: float = 1.0, timeout: float = 10) -> None:
        try:
            self._check(self.locate(course))
            self.cat("无须捡漏，抢课成功！")
        except ClassFull:
            pass
        except CourseConflict:
            self.cat("选课失败：志愿冲突！")
            return
        except TimeConflict:
            self.cat("选课失败：时间冲突！")
            return
        except AlreadyChoose:
            self.cat("选课失败：已经选择！")
            return
        
        self.cat("开始以间隔{}秒一次的速度持续捡漏...".format(pause_time))
        end_time = time.time() + timeout
        
        while time.time() <= end_time:
            info = self.locate(course, message=False)
            course_status = info["status"]
            if course_status.split('/')[0] == course_status.split('/')[1]:
                time.sleep(pause_time)
                continue
            else:
                try:
                    self._check(info)
                    self.cat("捡漏成功！")
                    return
                except ClassFull:
                    continue
        self.cat("超出设定时间，捡漏停止！")
        

    def quit(self) -> None:
        self._brower.quit()
    
    def __del__(self) -> None:
        self.__file.close()
