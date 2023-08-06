#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/9
"""
import time
import sys
import os


def lower_case_name(text):
    """
    将驼峰命名转为小写下划线命名
    :param text:
    :return:
    """
    lst = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            lst.append("_")
        lst.append(char)

    return "".join(lst).lower()


def log(text, *args):
    startup_debug = os.environ.get('FAST_DEBUG', 'off').lower() in ('on', 'true', '1')
    if startup_debug:
        text = text % args
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sys.stdout.write("FAST: %s (%d) - %s\n" % (timestamp, os.getpid(), text))
        sys.stdout.flush()
