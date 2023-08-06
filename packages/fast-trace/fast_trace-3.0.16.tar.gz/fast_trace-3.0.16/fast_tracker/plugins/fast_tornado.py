#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""
import json
from inspect import iscoroutinefunction, isawaitable

from fast_tracker import Layer, ComponentType, config
from fast_tracker.trace import tags
from fast_tracker.trace.carrier import Carrier
from fast_tracker.trace.context import get_context
from fast_tracker.trace.tags import Tag
from fast_tracker.utils.reader_type import ReaderType


def install():
    from tornado.web import RequestHandler

    old_execute = RequestHandler._execute
    old_log_exception = RequestHandler.log_exception
    RequestHandler._execute = _gen_fast_get_response_func(old_execute)

    def _fast_handler_uncaught_exception(self: RequestHandler, ty, value, tb, *args, **kwargs):
        if value is not None:
            entry_span = get_context().active_span()
            if entry_span is not None:
                entry_span.raised()

        return old_log_exception(self, ty, value, tb, *args, **kwargs)

    RequestHandler.log_exception = _fast_handler_uncaught_exception


def _gen_fast_get_response_func(old_execute):
    from tornado.gen import coroutine

    awaitable = iscoroutinefunction(old_execute)
    if awaitable:
        # Starting Tornado 6 RequestHandler._execute method is a standard Python coroutine (async/await)
        # In that case our method should be a coroutine function too
        async def _fast_get_response(self, *args, **kwargs):
            request = self.request
            context = get_context()
            carrier = Carrier()
            for item in carrier:
                if item.key.capitalize() in request.headers:
                    item.val = request.headers[item.key.capitalize()]
            with context.new_entry_span(op=request.path, carrier=carrier) as span:
                span.layer = Layer.Http
                span.component = ComponentType.Tornado
                peer = request.connection.stream.socket.getpeername()
                span.peer = "{0}:{1}".format(*peer)
                span.tag(Tag(key=tags.HttpMethod, val=request.method))
                span.tag(Tag(key=tags.HttpUrl, val="{}://{}{}".format(request.protocol, request.host, request.path)))
                # HttpPath 只需要获取PATH_INFO信息即可，不需要？后的内容
                span.tag(Tag(key=tags.HttpPath, val=(request.path).split("?")[0]))
                result = old_execute(self, *args, **kwargs)
                if isawaitable(result):
                    result = await result
                span.tag(Tag(key=tags.HttpStatus, val=self._status_code, overridable=True))
                if self._status_code >= 400:
                    span.error_occurred = True

                # tenant_code\user_code\env_code 根据配置动态获取并更新
                set_code(config.tenant_code_reader, request, "tenant_code")
                set_code(config.user_code_reader, request, "user_code")
                set_code(config.env_code_reader, request, "env_code")
            return result

    else:

        @coroutine
        def _fast_get_response(self, *args, **kwargs):
            request = self.request
            context = get_context()
            carrier = Carrier()
            for item in carrier:
                if item.key.capitalize() in request.headers:
                    item.val = request.headers[item.key.capitalize()]
            with context.new_entry_span(op=request.path, carrier=carrier) as span:
                span.layer = Layer.Http
                span.component = ComponentType.Tornado
                peer = request.connection.stream.socket.getpeername()
                span.peer = "{0}:{1}".format(*peer)
                span.tag(Tag(key=tags.HttpMethod, val=request.method))
                span.tag(Tag(key=tags.HttpUrl, val="{}://{}{}".format(request.protocol, request.host, request.path)))
                result = yield from old_execute(self, *args, **kwargs)
                span.tag(Tag(key=tags.HttpStatus, val=self._status_code, overridable=True))
                if self._status_code >= 400:
                    span.error_occurred = True

                set_code(config.tenant_code_reader, request, "tenant_code")
                set_code(config.user_code_reader, request, "user_code")
                set_code(config.env_code_reader, request, "env_code")
            return result

    return _fast_get_response


def set_code(reader, request, type="tenant_code"):
    """
    根据配置从不同渠道（cookie\header\querystring\env）获取tenant_code、user_code、env_code等数据
    :param reader:
    :param request:
    :param type:
    :return:
    """
    code = ""
    if not reader:
        return code

    reader_type = reader.get("ReaderType")
    reader_key = reader.get("ReaderKey")

    if reader_type == ReaderType.Cookie:
        code = request.get_cookie(reader_key, "")
    elif reader_type == ReaderType.RequestHeader:
        code = request.headers[reader_key] if reader_key in request.headers else ""
    elif reader_type == ReaderType.QueryString:
        # data = json.loads(request.body.decode('utf-8'))
        code = request.get_argument(reader_key, default="") if request.arguments.has_key(reader_key) else ""
    elif reader_type == ReaderType.Environment:
        import os

        code = os.getenv(reader.get("ReaderKey"), "")
    else:
        code = ""

    if code:
        # 设置config的code，让其全局适用
        if type == "tenant_code":
            config.set_tenant_code(code)
        elif type == "user_code":
            config.set_user_code(code)
        elif type == "env_code":
            config.set_env_code(code)

    return code
