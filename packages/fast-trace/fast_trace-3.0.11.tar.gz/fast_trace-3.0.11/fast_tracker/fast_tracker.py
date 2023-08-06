#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/12
"""
from fast_tracker import config, Layer, ComponentType, Log, LogItem
from fast_tracker.trace.context import get_context
from fast_tracker.trace.tags import Tag


class FastTracker:
    def __init__(self):
        self.span = None

    @staticmethod
    def set_enable(enable: bool = False):
        """
        设置enable值
        :param enable:
        :return:
        """
        config.set_enable(enable)

    @staticmethod
    def get_enable():
        """
        获取enable值
        :return:
        """
        return config.enable

    @staticmethod
    def set_env_code(env_code: str = ""):
        """
        设置env_code值
        :param env_code:
        :return:
        """
        config.set_env_code(env_code)

    @staticmethod
    def get_env_code():
        """
        获取 env_code 值
        :return:
        """
        return config.env_code

    @staticmethod
    def set_product_code(product_code: str = ""):
        """
        设置 product_code 值
        :param product_code:
        :return:
        """
        config.set_product_code(product_code)

    @staticmethod
    def get_product_code():
        """
        获取 product_code 值
        :return:
        """
        return config.product_code

    @staticmethod
    def set_app_code(app_code: str = ""):
        """
        设置 app_code 值
        :param app_code:
        :return:
        """
        config.set_app_code(app_code)

    @staticmethod
    def get_app_code():
        """
        获取 app_code 值
        :return:
        """
        return config.app_code

    @staticmethod
    def set_tenant_code(tenant_code: str = ""):
        """
        设置tenant_code值
        :param tenant_code:
        :return:
        """
        config.set_tenant_code(tenant_code)

    @staticmethod
    def get_tenant_code():
        """
        获取 tenant_code 值
        :return:
        """
        return config.tenant_code

    @staticmethod
    def set_user_code(user_code: str = ""):
        """
        设置user_code值
        :param user_code:
        :return:
        """
        config.set_user_code(user_code)

    @staticmethod
    def get_user_code():
        """
        获取 user_code 值
        :return:
        """
        return config.user_code

    @staticmethod
    def set_service_name(service_name: str = ""):
        """
        设置service_name值
        :param service_name:
        :return:
        """
        config.set_service_name(service_name)

    @staticmethod
    def get_service_name():
        """
        获取 service_name 值
        :return:
        """
        return config.service_name

    @staticmethod
    def set_socket_path(collector_address: str = ""):
        """
        设置collector_address值
        :param collector_address:
        :return:
        """
        config.set_socket_path(collector_address)

    @staticmethod
    def get_socket_path():
        """
        获取 socket_path 值
        :return:
        """
        return config.collector_address

    @staticmethod
    def set_buffer_size(buffer_size: int = 1):
        """
        设置buffer_size值
        :param buffer_size:
        :return:
        """
        config.set_buffer_size(buffer_size)

    @staticmethod
    def get_buffer_size():
        """
        获取 buffer_size 值
        :return:
        """
        return config.buffer_size

    @staticmethod
    def set_socket_timeout(socket_timeout: int = 1):
        """
        设置socket_timeout值
        :param socket_timeout:
        :return:
        """
        config.set_socket_timeout(socket_timeout)

    @staticmethod
    def get_socket_timeout():
        """
        获取 socket_timeout 值
        :return:
        """
        return config.socket_timeout

    @staticmethod
    def set_event(event: dict):
        """
        设置event值
        :param event:
        :return:
        """
        config.set_event(event)

    @staticmethod
    def get_event():
        """
        获取 event 值
        :return:
        """
        return config.event

    @staticmethod
    def set_tenant_code_reader(tenant_code_reader: dict):
        """
        设置tenant_code_reader值
        :param tenant_code_reader:
        :return:
        """
        config.set_tenant_code_reader(tenant_code_reader)

    @staticmethod
    def get_tenant_code_reader():
        """
        获取 tenant_code_reader 值
        :return:
        """
        return config.tenant_code_reader

    @staticmethod
    def set_user_code_reader(user_code_reader: dict):
        """
        设置user_code_reader值
        :param user_code_reader:
        :return:
        """
        config.set_user_code_reader(user_code_reader)

    @staticmethod
    def get_user_code_reader():
        """
        获取 user_code_reader 值
        :return:
        """
        return config.user_code_reader

    @staticmethod
    def set_carrier_header(carrier_header: dict):
        """
        设置carrier_header值
        :param carrier_header:
        :return:
        """
        config.set_carrier_header(carrier_header)

    @staticmethod
    def get_carrier_header():
        """
        获取 carrier_header 值
        :return:
        """
        return config.carrier_header

    @staticmethod
    def get_config():
        return {
            "ServiceName": config.service_name,
            "ServiceInstance": config.service_instance,
            "Protocol": config.protocol,
            "Authentication": config.authentication,
            "LogLevel": config.log_level,
            "DisablePlugins": config.disable_plugins,
            "IgnoreSuffix": config.ignore_suffix,
            "HttpParamsLengthThreshold": config.http_params_length_threshold,
            "DjangoCollectHttpParams": config.django_collect_http_params,
            "CorrelationElementMaxNumber": config.correlation_element_max_number,
            "CorrelationValueMaxLength": config.correlation_value_max_length,
            "TraceIgnorePath": config.trace_ignore_path,
            "Enable": config.enable,
            "EnvCode": config.env_code,
            "TenantCode": config.tenant_code,
            "UserCode": config.user_code,
            "SocketPath": config.collector_address,
            "BufferSize": config.buffer_size,
            "SocketTimeout": config.socket_timeout,
            "Event": config.event,
            "TenantCodeReader": config.tenant_code_reader,
            "UserCodeReader": config.user_code_reader,
            "CarrierHeader": config.carrier_header,
        }

    def begin_log(self):
        """
        log模块开始 类似数据库事务的begin_trasaction
        :return:
        """
        context = get_context()
        span = context.active_span()
        self.span = context.new_local_span(op="execute")
        self.span.layer = Layer.User
        self.span.component = ComponentType.User
        self.span.pid = span.sid
        self.span.start()
        return self
        # # with 语法后不需要start和stop 普通模式需要start和stop
        # with context.new_local_span(op="execute") as self.span:
        #     self.span.layer = Layer.User
        #     self.span.component = ComponentType.User
        #     self.span.pid = span.sid
        #     # self.span.start()
        #
        #     return self

    def debug(self, msg: str = ""):
        if not self.span:
            raise RuntimeError("请先调用begin_log实例化log对象")
        self.span.logs.append(Log(items=[LogItem(key="Debug", val=self.log_covert("Debug", msg))]))

    def info(self, msg: str = ""):
        if not self.span:
            raise RuntimeError("请先调用begin_log实例化log对象")
        self.span.logs.append(Log(items=[LogItem(key="Info", val=self.log_covert("Info", msg))]))

    def warning(self, msg: str = ""):
        if not self.span:
            raise RuntimeError("请先调用begin_log实例化log对象")
        self.span.logs.append(Log(items=[LogItem(key="Warning", val=self.log_covert("Warning", msg))]))

    def error(self, msg: str = ""):
        if not self.span:
            raise RuntimeError("请先调用begin_log实例化log对象")
        self.span.logs.append(Log(items=[LogItem(key="Error", val=self.log_covert("Error", msg))]))

    def critical(self, msg: str = ""):
        if not self.span:
            raise RuntimeError("请先调用begin_log实例化log对象")
        self.span.logs.append(Log(items=[LogItem(key="Critical", val=self.log_covert("Critical", msg))]))

    def log(self, msg: str = "", level: str = ""):
        if not self.span:
            raise RuntimeError("请先调用begin_log实例化log对象")
        self.span.logs.append(Log(items=[LogItem(key=level.capitalize(), val=self.log_covert(level, msg))]))

    def log_covert(self, level: str = "Debug", msg: str = ""):
        return {"err_msg": msg, "err_type": level, "err_trace": ""}

    def end_log(self):
        """
        log模块结束
        :return:
        """
        if not self.span:
            raise RuntimeError("请先调用begin_log实例化log对象")
        # with 语法后不需要start和stop 普通模式需要start和stop，取决于begin_log
        self.span.stop()
