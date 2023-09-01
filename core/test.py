import pathlib
import re
import time
from tqdm import tqdm

from core.file import read_all_file


# 模拟一个耗时操作，例如复制文件
def copy_file(source, destination):
    time.sleep(0.4)  # 模拟复制文件需要的时间
    # 在这里执行实际的文件复制操作


def test():
    # 定义要复制的文件列表
    files_to_copy = ['file1.txt', 'file2.txt', 'file3.txt', 'file2.txt', 'file3.txt', 'file2.txt', 'file3.txt']

    # 创建一个 tqdm 迭代器来显示进度条
    for file in tqdm(files_to_copy, desc="复制进度", unit="文件"):
        source_path = f"/path/to/source/{file}"
        destination_path = f"/path/to/destination/{file}"

        # 调用复制文件函数
        copy_file(source_path, destination_path)

    pbar = tqdm(range(300))  # 进度条

    for i in pbar:
        err = 'abc'
        time.sleep(0.4)  # 模拟复制文件需要的时间
        pbar.set_description("Reconstruction loss: %s" % (err))


def test2():
    pth = pathlib.Path(r"D:\work\src\TCq384manger")
    for e in pth.iterdir():
        if e.is_dir():
            print(e.absolute())
        elif e.is_file():
            print(e.absolute())

    print("------------------")
    for e in pth.glob("*"):
        if e.is_dir():
            print(e.absolute())
        elif e.is_file():
            print(e.absolute())
    # print(file.stat())
    # print(file.stat().st_size)
    # print(file.stat().st_atime)
    # print(file.stat().st_ctime)
    # print(file.stat().st_mtime)
    # print(file.parts, file.parent, file.parents)
    pass


if __name__ == '__main__':
    test2()
