"""
    定义日志方法
"""

import os
import logging
import time

from os import path
from logging.handlers import TimedRotatingFileHandler

DEFAULT_LOG_DIR = os.environ.get('APP_LOG_DIR', '/tmp')
DEFAULT_LOG_FILE_SIZE = 100 * 1024 * 1024


class MyTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
    扩展TimedRotatingFileHandler，支持大小+时间+压缩。
    """

    def __init__(self, filename, max_bytes=0, backup_count=0, encoding=None,
                 delay=0, when='h', interval=1, utc=False):
        TimedRotatingFileHandler.__init__(
            self, filename, when, interval, backup_count, encoding, delay, utc)

        self.max_bytes = max_bytes

    def shouldRollover(self, record):
        if self.stream is None:
            self.stream = self._open()

        # roll when exceeds the max_bytes
        if self.max_bytes > 0:
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= self.max_bytes:
                return 1

        if int(time.time()) >= self.rolloverAt:
            return 1

        return 0


def __create_logger(log_name, log_file_name=None, log_file_root=DEFAULT_LOG_DIR, log_level=logging.INFO):
    """

    :param log_name:
    :param log_file:
    :param log_root:
    :param level:
    :return:
    """
    this_logger = logging.getLogger(log_name)

    if not log_file_name:
        log_file_name = log_name

    this_logger.setLevel(log_level)

    if not path.exists(log_file_root):
        os.makedirs(log_file_root)

    file_handler = __create_log_file_handler('/'.join([log_file_root, log_file_name + '.log']), log_level)

    this_logger.addHandler(file_handler)
    return this_logger


def __create_log_file_handler(
        log_file,
        log_level,
        log_file_size=DEFAULT_LOG_FILE_SIZE,
        log_formatter=logging.Formatter(
            "%(asctime)s %(levelname)s %(filename)s.%(funcName)s:%(lineno)d - %(message)s")):
    """

    :param log_file_size: 默认100
    :param log_formatter:
    :return:
    """
    file_handler = MyTimedRotatingFileHandler(
        log_file, max_bytes=log_file_size, encoding='utf-8', backup_count=50)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_formatter)

    return file_handler

logger = __create_logger('app', log_level=logging.DEBUG)
