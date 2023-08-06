#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by iprobeyang@gmail.com 2021/4/13
"""

from django.http import HttpResponse


def hello(request):
    from django.shortcuts import redirect
    # redirect(index(request))
    redirect("http://localhost:8000/index")
    return HttpResponse("Hello world ! ")


def index(request):

    return HttpResponse("index")