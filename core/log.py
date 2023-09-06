import io
import logging
import os
import threading

import colorlog

from core import config, common


def init_log():
    # 创建一个 ColorLogFormatter 对象
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s[%(asctime)s] [%(levelname)s]: %(message)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    # 创建一个日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 创建一个处理程序并设置格式化程序
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # 将处理程序添加到记录器
    logger.addHandler(handler)
    if config.need_file_log():
        common.mkdir('log')
        global _file_log
        _file_log = open('log/file_log.txt', 'a', encoding='utf-8')
    return


_file_log: io.FileIO = {}
_file_lock = threading.Lock()


def close_file_log():
    global _file_log
    _file_log.close()


def write_file_log(data: str, file_modify: bool):
    if not file_modify and config.is_only_file_modify():
        # 如果只要记录改变的内容 并且文件没有发生变动，就不记录
        return
    global _file_lock
    global _file_log
    try:
        _file_lock.acquire(blocking=True)
        _file_log.write(data)
    finally:
        _file_lock.release()
