======================
天眼Python探针
======================


"fast_tracker" base on Apache SkyWalking Python agent and Newrelic Python:

https://github.com/newrelic/newrelic-python-agent

https://github.com/apache/skywalking-python

Installation
------------

.. code:: bash

    $ pip install fast-tracker

Usage
-----

1. 配置好配置文件FastTracker.json.



2. Validate the agent configuration and test the connection to our data collector service.

   .. code:: bash

      $ FAST_CONFIG_FILE=FastTracker.json fast-admin run-program $YOUR_COMMAND_OPTIONS

   Examples:

   .. code:: bash

      $ FAST_CONFIG_FILE=FastTracker.json FAST_STARTUP_DEBUG=true  fast-admin run-program hug -f app.py


License
-------

FAST for Python is free-to-use, proprietary software. Please see the LICENSE file in the distribution for details on the FAST License agreement and the licenses of its dependencies.

Copyright
---------

Copyright (c) 2019-2020 FAST, Inc. All rights reserved.