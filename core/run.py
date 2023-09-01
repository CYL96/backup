import logging
import os
import shutil
import sys
import _thread
import time

from tqdm import tqdm

from core import config, mult
from core import file


def run():
    # 备份

    logging.info('开始启动线程')

    # 创建进度条
    progress_bar = tqdm()  # progressBar
    progress_bar.unit = '个'

    # 开启线程 4个
    progress_bar.total = config.my_config.thread_num
    for i in range(config.my_config.thread_num):
        time.sleep(0.1)
        _thread.start_new_thread(mult.copy_file, (progress_bar, i))
    progress_bar.refresh()

    print('\n')
    time.sleep(1)
    logging.info('线程启动完成')
    time.sleep(1)
    logging.info('启动备份')
    for path in config.my_config.backup_path:
        # 开始递归文件和子文件
        from_f = file.get_all_file_dict(path.from_path, path.ignore_file, path.ignore_path)
        tp_f = file.get_all_file_dict(path.to_path, path.ignore_file, path.ignore_path)

        # print('\n')
        # time.sleep(0.5)
        logging.info(f'备份配置:{path.name}  文件数：{len(from_f)}')

        # 进度条调整
        progress_bar.reset(len(from_f))
        progress_bar.total = len(from_f)
        progress_bar.set_description(f'{path.name} ')

        # 开始进行文件对比
        for key in from_f:
            file_info = from_f[key]
            # 任务推送
            mult.message_queue.put(f'{key in tp_f},{file_info.full_path},{file_info.c_dir},{path.to_path}', block=True)
        # 等待任务完成
        mult.message_queue.join()
        progress_bar.refresh()

        # time.sleep(0.5)
        print('\n')
        time.sleep(0.5)
        logging.info(f'备份配置:{path.name}  文件数：{len(from_f)} --完成')

    print('\n')
    time.sleep(1)
    logging.info("全部完成")
