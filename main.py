from packs.secret import My, Desire
from common.setup import get_capabilities
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
        robber.rob_courses(Desire.rob_list)
        # robber.pick(Course("(2021-2022-2)-FL3201-47", "板块课(大学英语)"))
    except ProcessShutException:
        pass
    except Exception as e:
        raise e