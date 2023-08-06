#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by iprobeyang@gmail.com 2021/4/13
"""

from django.http import HttpResponse

from TestModel.models import Test


# 数据库操作
def testdb(request):
    test1 = Test(name='runoob')
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")