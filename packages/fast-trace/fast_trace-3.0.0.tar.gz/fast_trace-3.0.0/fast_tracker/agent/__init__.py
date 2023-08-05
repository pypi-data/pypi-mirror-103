#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""
import atexit
from queue import Queue, Full
from threading import Thread, Event
from typing import TYPE_CHECKING

from fast_tracker import config, plugins, loggings
from fast_tracker.loggings import logger
from fast_tracker.agent.protocol import Protocol

if TYPE_CHECKING:
    from fast_tracker.trace.context import Segment


def __heartbeat():
    while not __finished.is_set():  # 返回Event的内部标识是否为True，为True表示当前线程不阻塞
        if connected():
            __protocol.heartbeat()

        __finished.wait(30 if connected() else 3)


def __report():
    while not __finished.is_set():
        if connected():
            __protocol.report(__queue)  # is blocking actually
        __finished.wait(1)


# __heartbeat_thread = Thread(name='HeartbeatThread', target=__heartbeat, daemon=True)
__report_thread = Thread(name='ReportThread', target=__report, daemon=True)
__queue = Queue(maxsize=10000)
__finished = Event()
__protocol = Protocol()  # type: Protocol
__started = False


def __init():
    '''
    初始化插件
    :return:
    '''
    global __protocol
    if config.protocol == "udp":
        from fast_tracker.agent.protocol.udp import UdpProtocol
        __protocol = UdpProtocol()
    elif config.protocol == "http":
        from fast_tracker.agent.protocol.http import HttpProtocol
        __protocol = HttpProtocol()

    # plugins文件夹下面的所有插件都初始化（或者说是安装）
    plugins.install()


def __fini():
    __protocol.report(__queue, False)
    __queue.join()


def start():
    # 如果探针开关关闭,则不执行探针的初始化操作，不启动探针
    if not config.enable:
        return False
    flag = False
    try:
        # 猴子补丁，运行时动态替换
        from gevent import monkey
        flag = monkey.is_module_patched("socket")
    except ModuleNotFoundError:
        logger.debug("未发现使用gevent，如果确实未使用gevent，请忽略。")
    if flag:
        import grpc.experimental.gevent as grpc_gevent
        grpc_gevent.init_gevent()
    global __started
    if __started:
        raise RuntimeError('此代理只能启动一次')
    # 初始化log模块
    loggings.init()
    # 配置需要忽略的文件夹
    config.finalize()
    __started = True
    # 插件初始化
    __init()
    # 心跳线程启动
    # __heartbeat_thread.start()
    # 数据上报线程启动
    __report_thread.start()
    # atexit：退出处理器
    atexit.register(__fini)


def stop():
    atexit.unregister(__fini)
    __fini()
    __finished.set()


def started():
    return __started


def connected():
    return __protocol.connected()


def archive(segment: 'Segment'):
    try:  # unlike checking __queue.full() then inserting, this is atomic
        __queue.put(segment, block=False)
    except Full:
        logger.warning('队列已满，该segment将被放弃!')
