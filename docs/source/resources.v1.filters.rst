.. SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
..
.. SPDX-License-Identifier: MIT

Listing metrics given a SCM reference
-------------------------------------
Given a SCM reference, get all metrics linked to session referring to this reference.

    GET /api/v1/filters/scm/:scm/metrics

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| scm           | string   | yes      | A valid SCM reference.                  |
+---------------+----------+----------+-----------------------------------------+
| page          | integer  | No       | Directly jump to the requested page.    |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/filters/scm/2bdcf62f5cfaa71e9ede529ed4a43963e2d52d88/metrics

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

Counting metrics by SCM reference
---------------------------------
Count the number of metrics having a session with the specified SCM reference.

    GET /api/v1/filters/scm/:scm/metrics/count/

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| scm           | string   | yes      | A valid SCM reference.                  |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/filters/scm/2bdcf62f5cfaa71e9ede529ed4a43963e2d52d88/metrics/count/

Example response:

.. code-block:: json

   {
     "count": 42
   }

Counting metrics linked to a SCM reference
------------------------------------------
Count the number of metrics having a session with the given scm reference value set.

    GET /api/v1/filters/scm/:scm/metrics/count

Parameters
~~~~~~~~~~
None

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/filters/scm/2bdcf62f5cfaa71e9ede529ed4a43963e2d52d88/metrics/count

Example response:

.. code-block:: json

   {
    "count": 321
   }

Listing sessions associated to a SCM reference
----------------------------------------------
List all sessions whose scm reference match the one passed as a parameter.

    GET /api/v1/filters/scm/:scm/sessions

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| scm           | string   | yes      | A valid SCM reference.                  |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/filters/scm/2bdcf62f5cfaa71e9ede529ed4a43963e2d52d88/sessions

Example response:

.. code-block:: json

   {
    "sessions":
     [
      {"session_h": "0041724ff4e0adac62b70b4f810c79fc5ad8ba5b",
       "run_date": "2020-12-04T23:18:15.661016",
       "scm_ref": "2bdcf62f5cfaa71e9ede529ed4a43963e2d52d88",
       "tags": [
                { "key" : "numpy",
                  "value": "1.17.1"
                }
               ]
      },
      {"session_h": "417204ff40e0adac62b70b4f810c79fc5ad8ba5b",
       "run_date": "2020-12-04T23:18:15.661016",
       "scm_ref": "2bdcf62f5cfaa71e9ede529ed4a43963e2d52d88",
       "tags": [
                { "key" : "numpy",
                  "value": "1.17.2"
                },
                { "key" : "description",
                  "value": "Trying another numpy version."
                },
               ]
      }
     ],
    "prev_url": "/api/v1/sessions/?page=1",
    "next_url": "/api/v1/sessions/?page=3",
    "total_page": 3
   }


Listing metrics of a given scope (function, module ...)
-------------------------------------------------------
List all metrics given a scope. The scope represents the level at which `pytest-monitor` collects and aggregate data.

    GET /api/v1/filters/scope/:scope/metrics

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| scope         | string   | Yes      | Tests scope. Valid values are           |
|               |          |          |                                         |
|               |          |          |  - function                             |
|               |          |          |  - module                               |
|               |          |          |  - package                              |
+---------------+----------+----------+-----------------------------------------+
| page          | integer  | No       | Directly jump to the requested page.    |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/filters/scope/function/metrics

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

Counting metrics of a specific test entity (function, module ...)
-----------------------------------------------------------------
Count the number of metrics referenced under the specified scope.

    GET /api/v1/filters/scope/:scope/metrics/count

Parameters
~~~~~~~~~~
None

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/filters/scope/function/metrics/count

Example response:

.. code-block:: json

   {
    "count": 3210
   }
