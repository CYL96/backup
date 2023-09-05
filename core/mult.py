import datetime
import logging
import pathlib
import queue
import shutil
import time

from tqdm import tqdm

from core import common, log

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

        to_dir = common.build_path(to_path, c_dir)
        to_file = common.build_path(to_dir, file.name)
        log_content = f'{common.time_now()} {full_path} 至 {to_file}'
        log_not_change = False
        try:
            if exist == 'True':
                # 如果目标文件存在
                s_file = pathlib.Path(full_path).stat()
                t_file = pathlib.Path(to_file).stat()
                if s_file.st_size != t_file.st_size or s_file.st_mtime != t_file.st_mtime:
                    # 大小和修改时间不是一样，就替换文件
                    try:
                        log_content = f'覆盖成功 {log_content}\n'
                        shutil.copy2(full_path, to_file)
                    except (RuntimeError, TypeError, NameError) as err:
                        log_content = f'覆盖失败 {log_content} err:{err}\n'
                        logging.error(f'失败 :[{full_path} 至 {to_file}]\n----错误：{err}')
                        pass
                else:
                    log_not_change = True
                    log_content = f'存在跳过 {log_content}\n'
                continue
            else:

                try:
                    common.mkdir(to_dir)
                    # 调用复制文件函数
                    log_content = f'备份成功 {log_content}\n'
                    shutil.copy2(full_path, to_file)
                except (RuntimeError, TypeError, NameError) as err:
                    log_content = f'备份失败 {log_content} err:{err}\n'
                    logging.error(f'失败 :[{full_path} 至 {to_file}]\n----错误：{err}')
                    pass
        finally:
            message_queue.task_done()
            # 更新进度条
            progress_bar.update(1)
            log.write_file_log(log_content, log_not_change)
