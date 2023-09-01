import logging

import colorlog


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

    return
