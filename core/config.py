import json
import logging
import re

from core import common

# 全局的配置文件
backup_path = []
backup_to_path = str


class MyPathInfo:
    # from_path = ''  # 备份的路径
    # to_path = ''  # 备份到目标的路径

    def __init__(self, name: str, f_path: str, t_path: str, ignore_path: list[str], ignore_file: list[str]):
        self.name: str = name
        self.from_path: str = f_path
        self.to_path: str = t_path
        self.to_path: str = t_path
        self.to_path: str = t_path
        self.ignore_path: list[str] = ignore_path
        self.ignore_file: list[str] = ignore_file

    def check(self) -> bool:
        if self.from_path == '':
            logging.error('有配置未指定需要备份的文件夹')
            return False
        elif self.to_path == '':
            logging.error('有配置未指定备份的文件夹')
            return False
        logging.info(f'[{self.from_path}] >>==>> [{self.to_path}]')
        return True


class MyConfig:
    backup_path: list[MyPathInfo] = []

    def __init__(self, file_log: bool = False, only_file_modify: bool = False, thread_num: int = 4):
        self.backup_path = []
        self.file_log = file_log
        self.thread_num = thread_num
        self.only_file_modify = only_file_modify
        return

    def add_path_by_dict(self, data: dict):
        # ignore_path = data['ignore_path'],
        # ignore_file = data['ignore_file']
        name = data['name']
        f_path = data['from']
        t_path = data['to']
        ige_path: list[str] = []
        ige_file: list[str] = []
        # 正则表达式校验
        if 'ignore_path' in data:
            ige_path = data['ignore_path']

        if 'ignore_file' in data:
            ige_file = data['ignore_file']

        #    添加配置
        self.add_path(
            name=name,
            f_path=f_path,
            t_path=t_path,
            ignore_path=ige_path,
            ignore_file=ige_file,
        )

    def add_path(self, name: str, f_path: str, t_path: str, ignore_path: list[str], ignore_file: list[str]):
        self.backup_path.append(MyPathInfo(name, f_path, t_path, ignore_path, ignore_file))

    def check(self) -> bool:
        if len(self.backup_path) == 0:
            # 判断路径是不是空的
            logging.error('未指定备份目录')
            return False
        else:
            for e in self.backup_path:
                # 判断每个文件下面是不是空的
                if not e.check():
                    return False
        return True


my_config = MyConfig()


def need_file_log() -> bool:
    return my_config.file_log


def is_only_file_modify() -> bool:
    return my_config.only_file_modify


def readconfig(path: str):
    # 打开JSON文件并读取数据
    with open(path, 'r', encoding='utf-8') as file:
        config_data = json.load(file)
    global my_config
    if 'file_log' in config_data:
        my_config.file_log = config_data['file_log']

    if 'file_log_only_modify' in config_data:
        my_config.only_file_modify = config_data['file_log_only_modify']

    # 判断是否有错误
    logging.info("初始化备份配置")
    if 'backup_path' in config_data:
        config = config_data['backup_path']
        if len(config) == 0:
            raise ValueError("未指定备份配置")

        for e in config:
            if 'from' not in e:
                raise ValueError("未指定需要备份文件夹")
            if 'to' not in e:
                raise ValueError("未指定备份保存的文件夹")
            my_config.add_path_by_dict(e)
    else:
        raise ValueError("未指定备份配置")

    logging.info("初始化线程")
    if 'thread_num' in config_data:
        # print(config_data['thread_num'])
        num = config_data['thread_num']
        if num <= 0:
            num = 4
        if num > 32:
            num = 32
        my_config.thread_num = num
        logging.info(f'线程数量:{num}')


def backup():
    return
