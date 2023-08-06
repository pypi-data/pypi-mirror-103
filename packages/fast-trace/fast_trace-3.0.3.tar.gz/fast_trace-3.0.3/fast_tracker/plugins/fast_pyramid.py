#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from fast_tracker import Layer, ComponentType
from fast_tracker.trace import tags
from fast_tracker.trace.carrier import Carrier
from fast_tracker.trace.context import get_context
from fast_tracker.trace.tags import Tag


def install():
    from pyramid.router import Router

    def _fast_invoke_request(self, request, *args, **kwargs):
        context = get_context()
        carrier = Carrier()

        for item in carrier:
            val = request.headers.get(item.key)

            if val is not None:
                item.val = val

        with context.new_entry_span(op=request.path, carrier=carrier) as span:
            span.layer = Layer.Http
            span.component = ComponentType.Pyramid
            span.peer = request.remote_host or request.remote_addr

            span.tag(Tag(key=tags.HttpMethod, val=request.method))
            span.tag(Tag(key=tags.HttpUrl, val=str(request.url)))
            # HttpPath 只需要获取PATH_INFO信息即可，不需要？后的内容
            span.tag(Tag(key=tags.HttpPath, val=str(request.path)))

            resp = _invoke_request(self, request, *args, **kwargs)

            span.tag(Tag(key=tags.HttpStatus, val=resp.status_code, overridable=True))

            if resp.status_code >= 400:
                span.error_occurred = True

        return resp

    _invoke_request = Router.invoke_request
    Router.invoke_request = _fast_invoke_request
