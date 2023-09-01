import os
import pathlib
import re

from core import common


class MyFile:
    def equip(self, key: str) -> bool:
        return self.key == key

    def full_dir(self) -> str:
        return

    def __init__(self, path: str, c_dir: str, file: str):
        self.path = path  # 文件的路径
        self.c_dir = c_dir  # 文件所在的目录
        self.file = file  # 文件名
        self.key = common.build_path(c_dir, file)
        self.full_path = common.build_path(path, c_dir, file)

        file = pathlib.Path(self.full_path)
        self.size = file.stat().st_size  # 文件大小（以字节为单位）
        self.time = file.stat().st_mtime  # 文件时间戳
        # self.time = os.path.getmtime(self.full_path)  # 文件时间戳

    def __str__(self):
        return (
            f"File      : {self.file},\n"
            f"Size      : {self.size} bytes,\n"
            f"Full Path : {self.full_path},\n"
            f"Child Dir : {self.c_dir},\n"
            f"Time      : {self.time},\n"
            f"Key       : {self.key}")


def get_all_file_dict(path: str, ignore_file: list[str], ignore_path: list[str]) -> dict[str, MyFile]:
    f_list = read_all_file(path, ignore_file, ignore_path)
    info: dict[str, MyFile] = {}
    for e in f_list:
        info[e.key] = e
    return info


def read_all_file(path: str, ignore_file: list[str], ignore_path: list[str]) -> list[MyFile]:
    f = pathlib.Path(path)
    if f.is_file():
        file_info = MyFile(f.parent.absolute().__str__(), '', f.name)
        yield file_info
    else:
        for root, dirs, files in os.walk(path):
            f = pathlib.Path(root.replace(path, ""))
            for dir_name in dirs[:]:
                relative_path = f / dir_name
                # 匹配文件夹
                if any(relative_path.match(pattern) for pattern in ignore_path):
                    dirs.remove(dir_name)

            for file_name in files:
                if len(ignore_file) > 0:
                    # 匹配文件
                    file = pathlib.Path(common.build_path(root.replace(path, ""), file_name))
                    if not any(file.match(pattern) for pattern in ignore_file):
                        file_info = MyFile(path, root.replace(path, ""), file_name)
                        yield file_info
                else:
                    # print('-----------', file_name, root)
                    file_info = MyFile(path, root.replace(path, ""), file_name)
                    yield file_info
