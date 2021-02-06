# -*- coding: utf-8 -*-
import os
import logging

from combine import main


def log_init():
    logging.basicConfig(level=logging.CRITICAL,
                        format='%(asctime)s - %(filename)s[line: %(lineno)d] - %(levelname)s: %(message)s')
    logger = logging.getLogger()
    # log等級設置
    logger.setLevel(logging.INFO)

    if not os.path.isdir(r'./log'):
        os.makedirs(r'./log')
    filehander = logging.FileHandler(r'./log/loginfo.log', mode='a')

    filehander.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(filename)s[line: %(lineno)d] - %(levelname)s: %(message)s')
    filehander.setFormatter(formatter)
    logger.addHandler(filehander)


# pyside2-uic configuration_tool.ui -o configuration_tool.py
if __name__ == '__main__':
    log_init()
    main()
