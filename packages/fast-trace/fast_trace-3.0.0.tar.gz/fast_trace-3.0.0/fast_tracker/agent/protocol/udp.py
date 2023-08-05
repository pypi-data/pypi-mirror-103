#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""
from fast_tracker.loggings import logger
from queue import Queue, Empty

from fast_tracker.agent import Protocol
from fast_tracker.client.udp import UdpServiceManagementClient, UdpTraceSegmentReportService
from fast_tracker.trace.segment import Segment


class UdpProtocol(Protocol):
    def __init__(self):
        self.properties_sent = False
        self.service_management = UdpServiceManagementClient()
        self.traces_reporter = UdpTraceSegmentReportService()

    def heartbeat(self):
        if not self.properties_sent:
            self.service_management.send_instance_props()
            self.properties_sent = True
        self.service_management.send_heart_beat()

    def connected(self):
        return True

    def report(self, queue: Queue, block: bool = True):
        def generator():
            while True:
                try:
                    segment = queue.get(block=block)  # type: Segment
                except Empty:
                    return

                logger.debug('reporting segment %s', segment)

                yield segment

                queue.task_done()

        self.traces_reporter.report(generator=generator())
