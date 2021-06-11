.. SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
..
.. SPDX-License-Identifier: MIT

============
Installation
============

The `monitor-server-api` contains both the server and the API.
The server is based on:

 - `flask <https://flask.palletsprojects.com/en/1.1.x/>`_
 - `flask-restx <https://flask-restx.readthedocs.io/en/latest/>`_
 - `sqlalchemy <https://www.sqlalchemy.org/>`_
 - `uwsgi <https://uwsgi-docs.readthedocs.io/en/latest/>`_

On the other hand, the API requires the following to work:

 - `pyyaml <https://pypi.org/project/PyYAML/>`_
 - `requests <https://requests.readthedocs.io/en/master/>`_
 - `pandas <https://pandas.pydata.org/>`_

There is no way to get either the server or the api. Both systems are packaged together.

Supported environments
----------------------
The following versions of Python are supported:

 - Python 3.6
 - Python 3.7
 - Python 3.8

It currently runs on Linux. it hasn't been tested on Windows.

From conda
----------
Simply run the following command to get it installed in your current environment

.. code-block:: bash

    $ conda install monitor-server-api -c https://conda.anaconda.org/conda-forge

From pip
--------
Simply run the following command to get it installed

.. code-block:: bash

    $ pip install monitor-server-api