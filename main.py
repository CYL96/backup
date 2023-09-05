import json
import logging
import shutil

from core import (
    config,
    log,
    file,
    run
)


def main():
    logging.info('读取配置')
    try:
        config.readconfig('config.json')
    except ValueError as err:
        print(f'读取配置失败：{err}')

    log.init_log()

    logging.info('校验备份配置')
    if not config.my_config.check():
        return
    logging.info('校验备份配置-完成')

    run.run()


if __name__ == "__main__":
    # 当脚本直接运行时，执行main函数
    # shutil.copy2('D:\\code\python\\backup\\config.json.skip', "D:\\AAAAA\python\\backup\\config.json2")
    # for e in file.read_all_file('D:\\code\\python\\backup\\config.json.skip'):
    #     print(e)

    main()
