#!/usr/local/bin python3
# -*- coding: utf-8 -*-

import sys

import os
from setuptools import find_packages

python_version = sys.version_info[:2]

assert python_version in ((2, 7),) or python_version >= (3, 5), "天眼Python探针只支持 Python 2.7 and 3.5+."

with_setuptools = False

try:
    from setuptools import setup

    with_setuptools = True
except ImportError:
    from distutils.core import setup

from distutils.core import Extension
from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError

script_directory = os.path.dirname(__file__)
if not script_directory:
    script_directory = os.getcwd()

readme_file = os.path.join(script_directory, "README.rst")

if sys.platform == "win32" and python_version > (2, 6):
    build_ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError, IOError)
else:
    build_ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError)


class BuildExtFailed(Exception):
    pass


class optional_build_ext(build_ext):
    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError:
            raise BuildExtFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except build_ext_errors:
            raise BuildExtFailed()


# packages = [
#     "fast_tracker",
#     "fast_tracker.admin",
#     "fast_tracker.bootstrap",
#     "fast_tracker.common",
#     "fast_tracker.core",
#     "fast_tracker.client",
#     "fast_tracker.plugins",
#     "fast_tracker.report",
#     "fast_tracker.trace",
#     "fast_tracker/trace/ipc",
#     "fast_tracker/utils",
# ]

classifiers = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: System :: Monitoring",
]

kwargs = dict(
    name="fast_trace",
    version="3.0.0",
    setup_requires=["setuptools_scm"],
    description="FAST Python Agent",
    long_description=open(readme_file).read(),
    # long_description=README,
    url="http://doc.mypaas.com.cn/fast/03_%E6%9C%8D%E5%8A%A1%E7%AB%AF%E6%8E%A2%E9%92%88%E9%9B%86%E6%88%90/%E7%AE%80%E4%BB%8B.html",
    author="FAST",
    author_email="liulh01@mingyuanyun.com",
    maintainer="FAST",
    maintainer_email="liulh01@mingyuanyun.com",
    license="Apache-2.0",
    zip_safe=False,
    classifiers=classifiers,
    include_package_data=True,
    # packages=packages,
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        "grpcio",
        "grpcio-tools",
        "packaging",
    ],
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*",
    package_data={
        "fast_tracker": ["FastTracker.json"],
    },
    # package_data={'fast_tracker': ['FastTracker.json',
    #                                'version.txt',
    #                                'common/cacert.pem',
    #                                'packages/requests/LICENSE',
    #                                'packages/requests/NOTICE',
    #                                'packages/requests/cacert.pem'],
    #               },
    scripts=["scripts/fast-boot"],
    # extras_require={'infinite-tracing': ['grpcio<2', 'protobuf<4']},
    extras_require={
        "test": [
            "testcontainers",
            "pyyaml",
            "pytest",
        ],
        "http": [
            "requests",
        ],
        "kafka": [
            "kafka",
        ],
    },
)

if with_setuptools:
    kwargs["entry_points"] = {
        "console_scripts": ["fast-admin = fast_tracker.admin:main"],
    }


def with_librt():
    try:
        if sys.platform.startswith("linux"):
            import ctypes.util

            return ctypes.util.find_library("rt")
    except Exception:
        pass


def run_setup(with_extensions):
    def _run_setup():

        # Create a local copy of kwargs, if there is no c compiler run_setup
        # will need to be re-run, and these arguments can not be present.

        kwargs_tmp = dict(kwargs)

        if with_extensions:
            monotonic_libraries = []
            if with_librt():
                monotonic_libraries = ["rt"]

            kwargs_tmp["ext_modules"] = [
                Extension("fast_tracker.packages.wrapt._wrappers", ["fast_tracker/packages/wrapt/_wrappers.c"]),
                Extension(
                    "fast_tracker.common._monotonic",
                    ["fast_tracker/common/_monotonic.c"],
                    libraries=monotonic_libraries,
                ),
                Extension("fast_tracker.core._thread_utilization", ["fast_tracker/core/_thread_utilization.c"]),
            ]
            kwargs_tmp["cmdclass"] = dict(build_ext=optional_build_ext)

        setup(**kwargs_tmp)

    if os.environ.get("TDDIUM") is not None:
        try:
            print("INFO: Running under tddium. Use lock.")
            from lock_file import LockFile
        except ImportError:
            print("ERROR: Cannot import locking mechanism.")
            _run_setup()
        else:
            print("INFO: Attempting to create lock file.")
            with LockFile("setup.lock", wait=True):
                _run_setup()
    else:
        _run_setup()


WARNING = """
WARNING: The optional C extension components of the Python agent could
not be compiled. This can occur where a compiler is not present on the
target system or the Python installation does not have the corresponding
developer package installed. The Python agent will instead be installed
without the extensions. The consequence of this is that although the
Python agent will still run, some non core features of the Python agent,
such as capacity analysis instance busy metrics, will not be available.
Pure Python versions of code supporting some features, rather than the
optimised C versions, will also be used resulting in additional overheads.
"""

with_extensions = os.environ.get("FAST_EXTENSIONS", None)
if with_extensions:
    if with_extensions.lower() == "true":
        with_extensions = True
    elif with_extensions.lower() == "false":
        with_extensions = False
    else:
        with_extensions = None

if hasattr(sys, "pypy_version_info"):
    with_extensions = False

if with_extensions is not None:
    run_setup(with_extensions=with_extensions)

else:
    try:
        run_setup(with_extensions=True)

    except BuildExtFailed:

        print(75 * "*")

        print(WARNING)
        print("INFO: Trying to build without extensions.")

        print()
        print(75 * "*")

        run_setup(with_extensions=False)

        print(75 * "*")

        print(WARNING)
        print("INFO: Only pure Python agent was installed.")

        print()
        print(75 * "*")


# HERE = pathlib.Path(__file__).parent
#
# README = (HERE / "README.md").read_text()
#
# setup(
#     name="fast-tracker",
#     version="0.6.0",
#     description="Python Agent for FAST Tracker",
#     long_description=README,
#     long_description_content_type="text/markdown",
#     author="FAST",
#     author_email="fast@mingyuanyun.com",
#     license="Apache 2.0",
#     packages=find_packages(exclude=("tests",)),
#     include_package_data=True,
#     install_requires=[
#         "grpcio",
#         "grpcio-tools",
#         "packaging",
#     ],
#     extras_require={
#         "test": [
#             "testcontainers",
#             "pyyaml",
#             "pytest",
#         ],
#         "http": [
#             "requests",
#         ],
#         "kafka": [
#             "kafka",
#         ],
#     },
#     classifiers=[
#         "Framework :: Flake8",
#         "License :: OSI Approved :: Apache Software License",
#         "Operating System :: OS Independent",
#         "Programming Language :: Python",
#         "Programming Language :: Python :: 3",
#         "Programming Language :: Python :: 3.5",
#         "Programming Language :: Python :: 3.6",
#         "Programming Language :: Python :: 3.7",
#         "Programming Language :: Python :: 3.8",
#         "Topic :: Software Development",
#     ],
# )
