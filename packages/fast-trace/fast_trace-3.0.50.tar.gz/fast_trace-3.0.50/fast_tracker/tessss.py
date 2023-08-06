#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by iprobeyang@gmail.com 2021/4/27
"""

import requests
        # r = requests.get("https://www.baidu.com")
res = requests.get('http://www.baidu.com').content
print(res)
