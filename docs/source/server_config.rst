.. SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
..
.. SPDX-License-Identifier: MIT

=====
Setup
=====

.. tip::

    The `monitor-server` requires uwsgi to be served in a production environment.

Launching the server
====================
The server ships with a small utility script to help you launch the server and customize as much as possible the
different aspects of the run. The script, named `launch-monitor-server.sh` (Linux/Unix only) is accessible once
the `monitor-server-api` is installed.

If you are in a hurry, just type the following in your favorite terminal (we use conda for managing the environment):

.. code-block:: bash

    $ conda create -n monitor-server -c https://conda.anaconda.org/conda-forge monitor-server-api
    $ conda run -n monitor-server launch-monitor-server.sh

Running the above snippet will result in a server:

    - running on port 8181.
    - using a SQLLite database under the **current working directory**.
    - running without security layer, meaning that it will be accessible through HTTP.
    - using 4 workers.
    - running using production configuration

Customization
=============

A word about environments
-------------------------
The server is shipped with builtin configuration. Each configuration is intended to provide default values in
order to address a specific environment. Thus, two main environments can be identified:

 - The development environment
 - The production environment

Depending on the environment you want to address, the `monitor-server` needs instructions to setup
appropriate default values for the requested environment. This is achieved by setting the environment variable
**MONITOR_SERVER_ENV**. This environment variable's value is not case-sensitive.

+--------------------------+--------------------------+---------+
|   Requested environment  | Possible values          | Default |
+==========================+==========================+=========+
|   PRODUCTION             |  prod, production        |  X      |
+--------------------------+--------------------------+---------+
|   DEVELOPMENT            |  dev, devel, development |         |
+--------------------------+--------------------------+---------+

Changing the server's port
--------------------------
The server port default to 8181.
However, this can be customized via the launch script using the `-p` option:

.. code-block:: bash

    $ # Launch monitor-server on port 9090
    $ conda run -n monitor-server launch-monitor-server.sh -p 9090 
    
If you wish to change the default port while running in development mode, please consult the `flask documentation <https://flask.palletsprojects.com/en/1.0.x/config/#SERVER_NAME>`_.


Using HTTPS
-----------
Default schema used by the server is **http**. Obviously, you can choose to use **https**. For that, you will need to
instruct the `MONITOR_SERVER_CERTIFICATE` string to input paths to your certificates.

.. code-block:: bash

    $ export MONITOR_SERVER_CERTIFICATE="/etc/certs/host.cert.pki,/etc/certs/host.cert.pem"
    $ conda run -n monitor-server launch-monitor-server.sh


Mapping the  database
---------------------

Monitor servers provides an embedded SQLite datebase by default. You may change it's location or switch to a PosgreSQL RDBMS, strongly recommended for production environment.
This may be changed through `MONITOR_SERVER_DATABASE_URI` environment variable:

- for sqlite: sqlite:///<path>
- for postgres: postgre:///<url>

Pagination
----------
The `monitor-server` paginates results. By default, the size of a page contains up to 500 results.
You can increase (or decrease) the size of the page with the `MONITOR_SERVER_PAGINATION_COUNT` environment variable.

.. warning::

    Keep in mind that increasing the size of a page can harm the overall performance of the server. We strongly advise
    you to leave this value untouched.

.. code-block:: bash

    $ export MONITOR_SERVER_PAGINATION_COUNT=250
    $ conda run -n monitor-server launch-monitor-server.sh

Other possible customization
----------------------------

The launch script also support the following variable to help you customize the setup:

+----------------------------------+----------------+-----------------------------------------+
| Environment variable             | Default value  | Description                             |
+==================================+================+=========================================+
| MONITOR_SERVER_WORKERS           |   4            | Numbers of parallel workers             |
+----------------------------------+----------------+-----------------------------------------+
| MONITOR_SERVER_LOGDIR            |   $TMPDIR      | Path where to write the server logs     |
+----------------------------------+----------------+-----------------------------------------+

