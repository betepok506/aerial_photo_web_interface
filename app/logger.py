"""
Данный модуль содержит реализацию логера
"""

import logging
import logging.config


def get_file_handler():
    '''
    Функция для создания хандлера для вывода в файл
    `logging.FileHandler`
        Хандлер
    '''
    _log_format = "%(asctime)s\t%(levelname)s\t%(name)s\t" \
                  "%(filename)s.%(funcName)s " \
                  "line: %(lineno)d | \t%(message)s"
    file_handler = logging.FileHandler("logs/cache.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler