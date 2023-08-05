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
    from pymysql.cursors import Cursor

    _execute = Cursor.execute

    def _fast_execute(this: Cursor, query, args=None):
        peer = "%s:%s" % (this.connection.host, this.connection.port)

        context = get_context()
        with context.new_exit_span(op="Mysql/PyMsql/execute", peer=peer) as span:
            span.layer = Layer.Database
            span.component = ComponentType.PyMysql
            res = _execute(this, query, args)

            span.tag(Tag(key=tags.DbType, val="mysql"))
            span.tag(Tag(key=tags.DbInstance, val=(this.connection.db or b'').decode("utf-8")))
            span.tag(Tag(key=tags.DbStatement, val=query))

            parameter = ",".join([str(arg) for arg in args]) if args else ''
            span.tag(Tag(key=tags.DbSqlParameters, val='[' + parameter + ']'))

            print('#######mysql_span_output_start######')
            print(span)
            print('#######mysql_span_output_end######')

            return res

    Cursor.execute = _fast_execute
