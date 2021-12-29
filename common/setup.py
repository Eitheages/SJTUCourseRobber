import os
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver import DesiredCapabilities

def get_capabilities()->dict:
    """
    Add the proxy to capabilities,
    return a dict which contains brower's info along with the proxy.
    """
    myProxy = os.environ['https_proxy']

    proxy = Proxy(
        {
            'proxyType': ProxyType.MANUAL,
            'httpProxy': myProxy,
            'ftpProxy': myProxy,
            'sslProxy': myProxy,
            'noProxy':''
        }
    )

    capabilities = DesiredCapabilities.CHROME
    proxy.add_to_capabilities(capabilities)
    return capabilities
