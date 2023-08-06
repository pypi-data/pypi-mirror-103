from time import ctime

from fuzi.version import VERSION


def run():
    cur_time = ctime()
    text = f"""
    # fuzi
    
    Version {VERSION} ({cur_time} +0800)
    """
    print(text)
