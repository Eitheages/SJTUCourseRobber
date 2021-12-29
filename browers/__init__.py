import time

def nowtime() -> str:
    """Format the time now."""
    return time.strftime("%Y/%m/%d %H:%M:%S ", time.localtime())