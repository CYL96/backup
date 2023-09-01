import logging
import pathlib
import queue
import shutil
import time

from tqdm import tqdm

from core import common

message_queue = queue.Queue()


def copy_file(progress_bar: tqdm, num: int):
    # progress_bar 进度条对象
    # exist 文件是存在
    # full_path 完整路径
    # c_dir 子目录
    # to_path 备注目标文件夹

    progress_bar.set_description(f'线程[{num}]启动')
    progress_bar.update(1)

    while True:
        # message_queue.put()
        data = message_queue.get()
        if data == 'exit':
            message_queue.task_done()
            return

        lst = str(data).split(",")
        exist = lst[0]
        full_path = lst[1]
        c_dir = lst[2]
        to_path = lst[3]
        time.sleep(0.1)
        file = pathlib.Path(full_path)
        try:
            if exist == 'True':
                # 如果目标文件存在
                continue
            else:
                #
                to_dir = common.build_path(to_path, c_dir)
                to_file = common.build_path(to_dir, file.name)
                try:
                    common.mkdir(to_dir)
                    # 调用复制文件函数
                    shutil.copy2(full_path, to_file)
                except (RuntimeError, TypeError, NameError) as err:
                    logging.error(f'失败 :[{full_path} 至 {to_file}]\n----错误：{err}')
                    pass
        finally:
            message_queue.task_done()
            # 更新进度条
            progress_bar.update(1)
