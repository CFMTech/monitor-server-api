.. SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
..
.. SPDX-License-Identifier: MIT

List metrics for a specific variant
-----------------------------------
List all metrics of a test for a specific variant.

    GET /api/v1/variants/<string:variant>/metrics

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| variant       | string   | Yes      | Variant of the test.                    |
+---------------+----------+----------+-----------------------------------------+
| page          | integer  | No       | Directly jump to the requested page.    |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/variants/test_that_variant[x_2]/metrics

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
        "item": "test_that_variant",
        "item_variant": "test_that_variant[x_2]",
        "item_fs_loc": "tests/test_file.py",
        "kind": "function",
        "component": "server",
        "total_time": 0,
        "user_time": 0,
        "kernel_time": 0,
        "cpu_usage": 0,
        "mem_usage": 0
      },
      {
        "session_h": "1141724ff4e0adac62b70b4f810c79fc5ad8ba5b",
        "context_h": "fa188c68dd9ddeccd0a2f59422d16a2bf7337683",
        "item_start_time": "2020-12-04T23:19:15.661016",
        "item_path": "tests.test_file",
        "item": "test_that_variant",
        "item_variant": "test_that_variant[x_2]",
        "item_fs_loc": "tests/test_file.py",
        "kind": "function",
        "component": "server",
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


List metrics by test pattern
----------------------------
List all metrics for which the variant member match the given pattern.

    GET /api/v1/variants/like/:pattern/

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| pattern       | string   | Yes      | Pattern to use for filtering metrics.   |
+---------------+----------+----------+-----------------------------------------+
| page          | integer  | No       | Directly jump to the requested page.    |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/variants/like/test_server/metrics

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
        "item": "test_server_up",
        "item_variant": "test_server_up[]",
        "item_fs_loc": "tests/test_file.py",
        "kind": "function",
        "component": "server",
        "total_time": 0,
        "user_time": 0,
        "kernel_time": 0,
        "cpu_usage": 0,
        "mem_usage": 0
      },
      {
        "session_h": "0041724ff4e0adac62b70b4f810c79fc5ad8ba5b",
        "context_h": "e9188c68dd9ddeccd0a2f59422d16a2bf7337683",
        "item_start_time": "2020-12-04T23:18:15.661016",
        "item_path": "tests.test_file",
        "item": "test_server_ready",
        "item_variant": "test_server_ready[]",
        "item_fs_loc": "tests/test_file.py",
        "kind": "function",
        "component": "server",
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

Count all metrics for a given test
----------------------------------
Count all metrics entries having the given item variant.

    GET /api/v1/variants/<string:variant>/metrics/count

Parameters
~~~~~~~~~~
+---------------+----------+----------+--------------------------------------------+
| Attribute     | Type     | Required |  Description                               |
+===============+==========+==========+============================================+
| variant       | string   | Yes      | Full item variant of the requested test.   |
+---------------+----------+----------+--------------------------------------------+

Example
~~~~~~~

    $ curl -X GET https://monitor.instance.org/api/v1/variants/test_that[]/metrics/count

Example response:

.. code-block:: json

   {
    "count": 31
   }