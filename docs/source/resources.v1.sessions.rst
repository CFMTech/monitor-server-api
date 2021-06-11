.. SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
..
.. SPDX-License-Identifier: MIT

Create a session
----------------
Create a new session record by posting a JSON payload.

    POST /api/v1/sessions/

Parameters
~~~~~~~~~~
+-----------------+----------+----------+---------------------------------------------------+
| Attribute       | Type     | Required |  Description                                      |
+=================+==========+==========+===================================================+
| h               | string   | Yes      | Session id on which the test has been run.        |
+-----------------+----------+----------+---------------------------------------------------+
| run_date        | string   | Yes      | Date and time when test session has started.      |
|                 |          |          | Format: iso8601.                                  |
+-----------------+----------+----------+---------------------------------------------------+
| scm_ref         | string   | No       | Reference to the SCM if any.                      |
+-----------------+----------+----------+---------------------------------------------------+
| description     | string   | Yes      | Dictionary of tags:                               |
|                 |          |          |                                                   |
|                 |          |          | - All elements are of type string.                |
|                 |          |          | - Only dictionary with a depth of 1 is accepted.  |
+-----------------+----------+----------+---------------------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X POST --header "Content-Type: application/json" \
      --data '{"h": "0041724ff4e0adac62b70b4f810c79fc5ad8ba5b", \
               "run_date": "2020-12-04T23:18:15.661016", \
               "scm_ref": "4914d195225cf6b1c5a160c555b6948ea1ba2bcd", \
               "description": "\{"numpy": "1.17.1" \}"}'\
      https://monitor.instance.org/api/v1/sessions/

List all sessions
-----------------
List all sessions stored on the server.

    GET /api/v1/sessions/

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

    $ curl -X GET https://monitor.instance.org/api/v1/sessions/

Example response:

.. code-block:: json

   {
    "sessions":
     [
      {"session_h": "0041724ff4e0adac62b70b4f810c79fc5ad8ba5b",
       "run_date": "2020-12-04T23:18:15.661016",
       "scm_ref": "4914d195225cf6b1c5a160c555b6948ea1ba2bcd",
       "tags": [
                { "key" : "numpy",
                  "value": "1.17.1"
                }
               ]
      },
      {"session_h": "417204ff40e0adac62b70b4f810c79fc5ad8ba5b",
       "run_date": "2020-12-04T23:18:15.661016",
       "scm_ref": "d1952425cf6b19c5a1610c555b46948ea1ba2bcd",
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


Count sessions
--------------
Count all stored sessions.

    GET /api/v1/sessions/count/

Parameters
~~~~~~~~~~
None

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/sessions/count/

Example response:

.. code-block:: json

   {
     "count": 4256
   }


List metrics of a session
-------------------------
List all metrics linked to the specified session.

    GET /api/v1/session/:session/metrics/

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| session       | string   | Yes      | Full session identification key.        |
+---------------+----------+----------+-----------------------------------------+
| page          | integer  | No       | Directly jump to the requested page.    |
+---------------+----------+----------+-----------------------------------------+


Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/sessions/0041724ff4e0adac62b70b4f810c79fc5ad8ba5b/metrics/

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
    "prev_url": "/api/v1/contexts/0041724ff4e0adac62b70b4f810c79fc5ad8ba5b/metrics/?page=1",
    "next_url": "/api/v1/contexts/0041724ff4e0adac62b70b4f810c79fc5ad8ba5b/metrics/?page=3",
    "total_page": 3
   }

Count metrics of a session
--------------------------
Count the number of metrics having a session with the specified SCM reference.

    GET /api/v1/sessions/:session/metrics/count/

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| session       | string   | yes      | A valid session identification key.     |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/sessions/2bdcf62f5cfaa71e9ede529ed4a43963e2d52d88/metrics/count/

Example response:

.. code-block:: json

   {
     "count": 420
   }


Get session details
-------------------
List all sessions which have same identification key prefix.

    GET /api/v1/sessions/:session/

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| session       | string   | Yes      | Context identification key.             |
+---------------+----------+----------+-----------------------------------------+
| page          | integer  | No       | Directly jump to the requested page.    |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/sessions/0041724ff4e0

Example response:

.. code-block:: json

   {
    "sessions":
     [
      {"session_h": "0041724ff4e0adac62b70b4f810c79fc5ad8ba5b",
       "run_date": "2020-12-04T23:18:15.661016",
       "scm_ref": "4914d195225cf6b1c5a160c555b6948ea1ba2bcd",
       "tags": [
                { "key" : "numpy",
                  "value": "1.17.1"
                }
               ]
      },
      {"session_h": "0041724ff4e0eda589fec62b70b4f810c798ba5b",
       "run_date": "2020-12-04T23:18:15.661016",
       "scm_ref": "d1952425cf6b19c5a1610c555b46948ea1ba2bcd",
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
