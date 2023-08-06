#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from fast_tracker import Layer, ComponentType
from fast_tracker.trace import tags
from fast_tracker.trace.context import get_context
from fast_tracker.trace.tags import Tag


def install():
    print("r1")
    from redis.connection import Connection
    print("r2")

    _send_command = Connection.send_command

    def _fast_send_command(this: Connection, *args, **kwargs):
        print("r3")
        peer = "%s:%s" % (this.host, this.port)
        op = args[0]
        context = get_context()
        print("r4")
        with context.new_exit_span(op="Redis/" + op or "/", peer=peer) as span:
            print("r5")
            span.layer = Layer.Cache
            span.component = ComponentType.Redis
            print("r6")
            res = _send_command(this, *args, **kwargs)
            print("r7")
            span.tag(Tag(key=tags.CacheType, val=ComponentType.Redis))
            span.tag(Tag(key=tags.CacheInstance, val=this.db))
            span.tag(Tag(key=tags.CacheCommand, val=op))
            print("r8")

            return res

    print("r9")

    Connection.send_command = _fast_send_command
