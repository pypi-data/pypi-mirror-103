#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from fast_tracker import Layer, ComponentType, config
from fast_tracker.trace import tags
from fast_tracker.trace.carrier import Carrier
from fast_tracker.trace.context import get_context
from fast_tracker.trace.tags import Tag
from fast_tracker.utils.reader_type import ReaderType


def install():
    from aiohttp import ClientSession
    from aiohttp.web_protocol import RequestHandler
    from multidict import CIMultiDict, MultiDict, MultiDictProxy
    from yarl import URL

    async def _fast_request(self: ClientSession, method: str, str_or_url, **kwargs):
        url = URL(str_or_url).with_user(None).with_password(None)
        peer = "%s:%d" % (url.host or "", url.port)
        context = get_context()

        with context.new_exit_span(op=url.path or "/", peer=peer) as span:
            span.layer = Layer.Http
            span.component = ComponentType.AioHttp
            span.tag(Tag(key=tags.HttpMethod, val=method.upper()))  # pyre-ignore
            span.tag(Tag(key=tags.HttpUrl, val=url))  # pyre-ignore
            # HttpPath 只需要获取PATH_INFO信息即可，不需要？后的内容
            span.tag(Tag(key=tags.HttpPath, val=url.path))  # pyre-ignore

            carrier = span.inject()
            headers = kwargs.get("headers")

            if headers is None:
                headers = kwargs["headers"] = CIMultiDict()
            elif not isinstance(headers, (MultiDictProxy, MultiDict)):
                headers = CIMultiDict(headers)

            for item in carrier:
                headers.add(item.key, item.val)

            res = await _request(self, method, str_or_url, **kwargs)

            span.tag(Tag(key=tags.HttpStatus, val=res.status, overridable=True))

            if res.status >= 400:
                span.error_occurred = True

            return res

    _request = ClientSession._request
    ClientSession._request = _fast_request

    async def _fast_handle_request(self, request, start_time: float):
        context = get_context()
        carrier = Carrier()

        for item in carrier:
            val = request.headers.get(item.key)

            if val is not None:
                item.val = val

        with context.new_entry_span(op=request.path, carrier=carrier) as span:
            span.layer = Layer.Http
            span.component = ComponentType.AioHttp
            span.peer = (
                "%s:%d" % request._transport_peername
                if isinstance(request._transport_peername, (list, tuple))
                else request._transport_peername
            )

            span.tag(Tag(key=tags.HttpMethod, val=request.method))  # pyre-ignore
            span.tag(Tag(key=tags.HttpUrl, val=str(request.url)))  # pyre-ignore

            resp, reset = await _handle_request(self, request, start_time)

            span.tag(Tag(key=tags.HttpStatus, val=resp.status, overridable=True))

            # tenant_code\user_code\env_code 根据配置动态获取并更新
            # async with self.get(request.url) as response:
            #     cookies = response.cookies
            set_code(config.tenant_code_reader, request, resp, "tenant_code")
            set_code(config.user_code_reader, request, resp, "user_code")
            set_code(config.env_code_reader, request, resp, "env_code")

            if resp.status >= 400:
                span.error_occurred = True

        return resp, reset

    def set_code(reader, request, response, type="tenant_code"):
        """
        根据配置从不同渠道（cookie\header\querystring\env）获取tenant_code、user_code、env_code等数据
        :param reader:
        :param request:
        :param response:
        :param type:
        :return:
        """
        # TODO 因未有团队使用此框架，故未进行完整测试
        code = ""
        if not reader:
            return code

        reader_type = reader.get("ReaderType")
        reader_key = reader.get("ReaderKey")

        if reader_type == ReaderType.Cookie:
            # TODO cookie 未进行测试 ref:https://docs.aiohttp.org/en/stable/client_advanced.html
            code = response.cookies.get(reader_key, "")
        elif reader_type == ReaderType.RequestHeader:
            code = request.headers[reader_key] if reader_key in request.headers else ""
        elif reader_type == ReaderType.QueryString:
            if request.method == "GET":
                code = request.get().get(reader_key, default="")
            elif request.method == "POST":
                code = request.post().get(reader_key, default="")
        elif reader_type == ReaderType.Environment:
            import os

            code = os.getenv(reader_key, "")
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

    _handle_request = RequestHandler._handle_request
    RequestHandler._handle_request = _fast_handle_request
