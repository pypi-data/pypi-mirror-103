#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""
import logging
from fast_tracker import Layer, ComponentType, Log, LogItem, config
from fast_tracker.trace.context import get_context


log_level = {"NOTSET": 0, "DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}


def install():
    """
    python日志拦截器
    lib/python3.8/loggin/__init__.py中已定义日志等级:
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0
    :return:
    """
    _handle = logging.Logger._log

    def params_tostring(msg, level):
        return {"err_msg": msg, "err_type": level, "err_trace": ""}

    def _fast_handle(this: logging.Logger, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        if log_level.get(config.log_level) <= level:
            context = get_context()
            with context.new_exit_span(op="Log", peer="") as span:
                span.layer = Layer.Log
                span.component = ComponentType.Log

                data = params_tostring(msg, level)
                level_names = {v:k for k, v in log_level.items()}
                span.logs.append(Log(items=[LogItem(key=level_names.get(level, "USER_UNKNOWN"), val=data)]))

                res = _handle(this, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1)

                return res
        else:
            # 当配置文件中的配置的日记级别高于当前上报日志级别，则不做探针上报，也就是说拦截器什么都不做，只负责调用日志原始处理器
            res = _handle(this, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1)

            return res

    logging.Logger._log = _fast_handle
