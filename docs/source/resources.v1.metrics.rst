.. SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
..
.. SPDX-License-Identifier: MIT

Create a metric
---------------
Create a new metric record by posting a JSON payload.

    POST /api/v1/metrics/

Parameters
~~~~~~~~~~
+-----------------+----------+----------+---------------------------------------------------+
| Attribute       | Type     | Required |  Description                                      |
+=================+==========+==========+===================================================+
| session_h       | string   | Yes      | Session id of the test.                           |
+-----------------+----------+----------+---------------------------------------------------+
| ctx_h           | string   | Yes      | ExecutionContext id of the test.                  |
+-----------------+----------+----------+---------------------------------------------------+
| item_start_time | string   | Yes      | Effective start time of the test. Format: iso8601 |
+-----------------+----------+----------+---------------------------------------------------+
| item_path       | string   | Yes      | Path of the item using Python                     |
|                 |          |          | import specification.                             |
+-----------------+----------+----------+---------------------------------------------------+
| item            | string   | Yes      | Fully qualified name of the test.                 |
+-----------------+----------+----------+---------------------------------------------------+
| item_variant    | string   | Yes      | Fully qualified name of the test with             |
|                 |          |          | parametrization info.                             |
+-----------------+----------+----------+---------------------------------------------------+
| item_fs_loc     | string   | Yes      | Relative path from pytest invocation              |
|                 |          |          | directory to the item's module..                  |
+-----------------+----------+----------+---------------------------------------------------+
| kind            | string   | Yes      | Item type (class, function, module...)            |
+-----------------+----------+----------+---------------------------------------------------+
| component       | string   | Yes      | Component to which the test belong.               |
+-----------------+----------+----------+---------------------------------------------------+
| wall_time       | float    | Yes      | Total time spent running the test (in seconds).   |
+-----------------+----------+----------+---------------------------------------------------+
| user_time       | float    | Yes      | Total time spent running in user space.           |
|                 |          |          | Unit expressed in seconds.                        |
+-----------------+----------+----------+---------------------------------------------------+
| krnl_time       | float    | Yes      | Total time spent running in kernel mode.          |
|                 |          |          | Unit expressed in seconds.                        |
+-----------------+----------+----------+---------------------------------------------------+
| cpu_usage       | float    | Yes      | Percentage of CPU used while the test ran.        |
+-----------------+----------+----------+---------------------------------------------------+
| mem_usage       | float    | Yes      | Memory used while running the test (in MB).       |
+-----------------+----------+----------+---------------------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X POST --header "Content-Type: application/json" \
      --data '{"session_h": "0041724ff4e0adac62b70b4f810c79fc5ad8ba5b", \
               "ctx_h": "e9188c68dd9ddeccd0a2f59422d16a2bf7337683", \
               "item_start_time": "2020-12-04T23:18:15.661016", \
               "item_path": "tests.test_file", "item": "test_that", \
               "item_variant": "test_that[]", "item_fs_loc": "tests/test_file.py", \
               "kind": "function", "component": "test_component", \
               "wall_time": 0, "user_time": 0, "krnl_time": 0, \
               "cpu_usage": 0, "mem_usage": 0}'\
      https://monitor.instance.org/api/v1/metrics/

List metrics
------------
List all stored metrics the `monitor-server` instance has access to.

    GET /api/v1/metrics/

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| page          | integer  | No       | Directly jump to the requested page.    |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/metrics/

Example response:

.. code-block:: json

   {
    "metrics":
    [
      {
        "session_h": "0041724ff4e0adac62b70b4f810c79fc5ad8ba5b",
        "context_h": "e9188c68dd9ddeccd0a2f59422d16a2bf7337683",
        "item_start_time": "2020-12-04T23:18:15.661016",
        "item_path": "tests.test_file",
        "item": "test_that",
        "item_variant": "test_that[]",
        "item_fs_loc": "tests/test_file.py",
        "kind": "function",
        "component": "test_component",
        "total_time": 0,
        "user_time": 0,
        "kernel_time": 0,
        "cpu_usage": 0,
        "mem_usage": 0
      }
    ],
    "prev_url": "/api/v1/metrics/?page=1",
    "next_url": "/api/v1/metrics/?page=3",
    "total_page": 3
   }

Counting metrics
----------------
Count all stored metrics.

    GET /api/v1/metrics/count/

Parameters
~~~~~~~~~~
None

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/metrics/count/

Example response:

.. code-block:: json

   {
     "count": 12345
   }
