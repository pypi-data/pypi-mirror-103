#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/7
"""
import sys
import os
# print(os.path.dirname(sys.path[0]))
# print("/Users/yangzhengyuan/work/my/fast/code/fast-tracker-sw-python/venv/lib/python3.8")
# exit()
sys.path.append("/Users/yangzhengyuan/work/my/fast/code/fast-tracker-sw-python")
# sys.path.append(os.path.dirname(sys.path[0]))
# if __name__ == '__main__':
#     print(os.path.dirname(sys.path[0]))
#     exit()
#     sys.path.append(os.path.dirname(sys.path[0]))

import hug
from fast_tracker import agent, config

# print(config)
# exit()


# SW_AGENT_PROTOCOL = 'http'
config.init(collector='127.0.0.1:11800', service='your awesome service')
# config.init(collector='127.0.0.1:5140', service='your awesome service')
agent.start()


@hug.get('/hello')
def hello():
    '''say hello'''
    return 'hello'