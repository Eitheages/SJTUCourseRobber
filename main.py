from packs.secret import *
from common.setup import *
from exceptions import *
from browers import chrome

'''
Every function contains several "assert" statements, which avoid most possible exceptions.
It's important to take every break, specifically saying, time.sleep().
'''

if __name__ == "__main__":
    capabilities = get_capabilities()
    try:
        robber = chrome.CourseRobber(capabilities, My.account, My.password)
        robber.login(cookies=My.cookies)
        robber.jump()
        e = robber.locate(Course("(2021-2022-2)-EN356-1", "任选课程"))
        robber.check(e)
    except Exception as e:
        print(e)