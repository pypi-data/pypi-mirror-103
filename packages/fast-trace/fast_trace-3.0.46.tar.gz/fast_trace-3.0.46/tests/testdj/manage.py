#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import sys
import os
# print(os.path.dirname(sys.path[0]))
# print("/Users/yangzhengyuan/work/my/fast/code/fast-tracker-sw-python/venv/lib/python3.8")
# exit()



sys.path.append("/Users/yangzhengyuan/work/my/fast/code/fast-tracker-sw-python")
# sys.path.append(os.path.dirname(sys.path[0]))
# if __name__ == '__main__':
#     print(os.path.dirname(sys.path[0]))
#     exit()
#     sys.path.append(os.path.dirname(sys.path[0]))

from fast_tracker import agent, config, Component
from fast_tracker.trace.tags import Tag

# print(config)
# exit()


# SW_AGENT_PROTOCOL = 'http'
config.init(collector='127.0.0.1:11800', service='your awesome service')
# config.init(collector='127.0.0.1:5140', service='your awesome service')
agent.start()
# print("1111111111111111")
# exit()

import os
import sys


'''
单个方法追踪模式：
from fast_tracker.decorators import trace

@trace()
'''
# from fast_tracker.decorators import trace
# from fast_tracker.trace.context import get_context
#
# @trace()
def main():
    # context: SpanContext = get_context()
    print("mmmmmmmmmmm")

    # with context.new_entry_span(op="https://github.com/apache") as span:
    #     span.component = Component.Django
    #     span.tag(Tag(key='Org', val="Apache"))
    #     print("xxxxxxxxxxxxxxxxx")
    # print("zzzzzzzzzzzzzzzzzzzzzzzz")




    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testdj.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
