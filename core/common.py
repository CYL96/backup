import _thread
import os
import re
import sys
from pathlib import Path


def build_path(*args) -> str:
    prefix = '/'
    if sys.platform.startswith('win'):
        prefix = "\\"
    result: str = ""
    for arg in args:
        # 合并路径
        arg = arg.rstrip(prefix)
        if result != '':
            arg = arg.lstrip(prefix)
            result = result + prefix + arg
        else:
            result = arg
    return result


lock = _thread.allocate_lock()


def mkdir(path: str):
    lock.acquire()
    try:
        # 创建目录
        if not os.path.exists(path):
            os.makedirs(path)
            # print(f"目录 {path} 创建成功")
    finally:
        lock.release()


if __name__ == "__main__":
    a = build_path('aaa\\b', 'bbb')
    print(a)
