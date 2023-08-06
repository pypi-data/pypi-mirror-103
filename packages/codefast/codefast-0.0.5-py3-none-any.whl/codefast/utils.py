# coding:utf-8
import csv
import json
import random
import signal
import subprocess
import sys
import time
from functools import wraps
from pprint import pprint
from typing import List, Union

import requests
import smart_open

from .logger import Logger


# =========================================================== display
def p(*s):
    for i in s:
        print(i)


def pp(d: dict):
    pprint(d)


def sleep(countdown: int) -> None:
    time.sleep(countdown)


def random_sleep(lower_bound: int, upper_bound: int) -> None:
    """Randomly sleep for few seconds. Typical usage involving a crontab task
    to prevent robot behavior detection.
    """
    time.sleep(random.randint(lower_bound, upper_bound))


# =========================================================== IO
def show_func_name():
    p(f"\n--------------- {sys._getframe(1).f_code.co_name} ---------------")


def smartopen(file_path: str):
    with smart_open.open(file_path) as f:
        return f.readlines()


def info(msg):
    Logger().info(msg)


def debug(msg):
    Logger().debug(msg)


def warning(msg):
    Logger().warning(msg)


def error(msg):
    Logger().error(msg)


def critical(msg):
    Logger().critical(msg)


def shell(cmd: str, print_str: bool = False) -> str:
    ret_str = ''
    try:
        ret_str = subprocess.check_output(cmd,
                                          stderr=subprocess.STDOUT,
                                          shell=True).decode('utf8')
    except Exception as e:
        print(e)
    finally:
        if print_str:
            p(ret_str)
        return ret_str


class TextIO:
    @staticmethod
    def read(file_name: str, delimiter: str = '') -> Union[str, list]:
        texts = open(file_name, 'r').read().__str__()
        if delimiter:
            return texts.strip().split(delimiter)
        return texts

    @staticmethod
    def write(cons: str, file_name: str) -> None:
        with open(file_name, 'w') as f:
            f.write(cons)

    @staticmethod
    def say(contents):
        pprint(contents)


class JsonIO:
    @staticmethod
    def read(file_name: str) -> dict:
        res = {}
        with open(file_name, 'r') as f:
            res = json.loads(f.read())
        return res

    @staticmethod
    def write(d: dict, file_name: str):
        json.dump(d, open(file_name, 'w'), ensure_ascii=False, indent=2)

    @staticmethod
    def eval(file_name: str) -> dict:
        '''Helpful parsing single quoted dict'''
        return eval(TextIO.read(file_name))


class CSVIO:
    @classmethod
    def read(cls, filename: str, delimiter: str = ',') -> List[List]:
        ''' read a CSV file and export it to a list '''
        texts = []
        with open(filename, newline='') as f:
            for row in csv.reader(f, delimiter=delimiter):
                texts.append(row)
        return texts

    @classmethod
    def iterator(cls, filename: str, delimiter: str = ',') -> csv.reader:
        return csv.reader(open(filename, 'r').readlines(),
                          delimiter=delimiter,
                          quoting=csv.QUOTE_MINIMAL)

    @classmethod
    def write(cls,
              texts: List,
              filename: str,
              delimiter: str = ',',
              column: int = 0) -> None:
        with open(filename, mode='w') as f:
            wt = csv.writer(f,
                            delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
            for row in texts:
                if column > 0:
                    n_row = row[:column - 1]
                    n_row.append(' '.join(row[column - 1:]))
                    n_row = [e.strip() for e in n_row]
                    wt.writerow(n_row)
                else:
                    wt.writerow(row)

# =========================================================== Decorator
def set_timeout(countdown: int, callback=print):
    def decorator(func):
        def handle(signum, frame):
            raise RuntimeError

        def wrapper(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)
                signal.alarm(countdown)  # set countdown
                r = func(*args, **kwargs)
                signal.alarm(0)  # close alarm
                return r
            except RuntimeError as e:
                print(e)
                callback()

        return wrapper

    return decorator


def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result

    return wrapper


def logged(logger_func, name=None, message=None):
    """
    Add logging to a function. name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.
    """
    import logging

    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            logger_func(logmsg)
            return func(*args, **kwargs)

        return wrapper

    return decorate


class Network:
    @staticmethod
    def get(url: str) -> requests.models.Response:
        return requests.get(url)

    @staticmethod
    def post(url: str,
             param: dict,
             post_format='json') -> requests.models.Response:
        if post_format == 'json':
            return requests.post(url, json=param)
        else:
            return requests.post(url, data=param)
