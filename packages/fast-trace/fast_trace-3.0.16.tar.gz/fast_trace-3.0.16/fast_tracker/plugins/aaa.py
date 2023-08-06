
#!/usr/local/bin python3
# -*- coding: utf-8 -*-



#!/usr/bin/python
# import sys
# print(sys.version)
# print(sys.version_info)

# #!/usr/bin/python
# import platform
# python_version = platform.python_version()
# if python_version >= 3.8:
#     print("dddd")
# else:
#     print("yes")

# 检查你的Python版本
from sys import version_info
if version_info.major >= 3 :
    print("dees")
    if version_info.minor == 5:
        print("eeee")
        raise Exception('请使用Python 2.7来完成此项目')
    elif version_info.minor == 8:
        print("dssfas")
