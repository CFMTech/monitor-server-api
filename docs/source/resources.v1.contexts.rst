.. SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
..
.. SPDX-License-Identifier: MIT

Create a context
----------------
Create a new execution context by posting JSON payload

    POST /api/v1/contexts/

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| h             | string   | Yes      | Unique context identifier.              |
+---------------+----------+----------+-----------------------------------------+
| cpu_count     | integer  | Yes      | Number of available CPU.                |
+---------------+----------+----------+-----------------------------------------+
| cpu_freq      | integer  | Yes      | Nominal frequency of a CPU, in MHz.     |
+---------------+----------+----------+-----------------------------------------+
| cpu_type      | string   | Yes      | Architecture of the CPU.                |
+---------------+----------+----------+-----------------------------------------+
| cpu_vendor    | string   | No       | Information about constructor.          |
+---------------+----------+----------+-----------------------------------------+
| ram_total     | integer  | Yes      | Total RAM available, in MB.             |
+---------------+----------+----------+-----------------------------------------+
| mac_node      | string   | Yes      | Fully Qualified Domain Name (FQDN)      |
|               |          |          | of the machine used for testing         |
+---------------+----------+----------+-----------------------------------------+
| mac_type      | string   | Yes      | Machine architecture.                   |
+---------------+----------+----------+-----------------------------------------+
| mac_arch      | string   | Yes      | Bitmode of the machine.                 |
+---------------+----------+----------+-----------------------------------------+
| sys_info      | string   | Yes      | Short string about the Operating System.|
+---------------+----------+----------+-----------------------------------------+
| py_info       | string   | Yes      | Python information                      |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X POST --header "Content-Type: application/json" \
      --data '{"h": "0041724ff4e0adac62b70b4f810c79fc5ad8ba5b", \
               "cpu_count": 8, "cpu_freq": 2500, "cpu_type": "i386",
               "ram_total": 16384, "mac_node": "host.name.org", "mac_type": "x86_64", \
               "max_arch": "64bit", "sys_info": "Linux - 3.10.0-693.el7.x86_64", \
               "py_info": "3.6.10 packaged by conda-forge"}'\
      https://monitor.instance.org/api/v1/contexts/

List contexts
-------------
List all known execution contexts.

    GET /api/v1/contexts/

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

    $ curl -X GET https://monitor.instance.org/api/v1/contexts/

Example response:

.. code-block:: json

   {
    "contexts":
     [
      {
        "h": "0041724ff4e0adac62b70b4f810c79fc5ad8ba5b",
        "cpu_count": 8,
        "cpu_frequency": 2500,
        "cpu_type": "i386",
        "cpu_vendor": "",
        "ram_total": 16384,
        "machine_node": "host.name.org",
        "machine_type": "x86_64",
        "machine_arch": "64bit",
        "system_info": "Linux - 3.10.0-693.el7.x86_64",
        "python_info": "3.6.10 packaged by conda-forge"
      }
     ],
    "prev_url": "/api/v1/contexts/?page=1",
    "next_url": "/api/v1/contexts/?page=3",
    "total_page": 3
   }


Count contexts
--------------
Count all stored contexts.

    GET /api/v1/contexts/count/

Parameters
~~~~~~~~~~
None

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/contexts/count/

Example response:

.. code-block:: json

   {
     "count": 12
   }

List metrics of a context
-------------------------
List all metrics linked to the specified context.

    GET /api/v1/contexts/:context/metrics/

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| context       | string   | Yes      | Full context identification key.        |
+---------------+----------+----------+-----------------------------------------+
| page          | integer  | No       | Directly jump to the requested page.    |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/contexts/0041724ff4e0adac62b70b4f810c79fc5ad8ba5b/metrics/

Example response:

.. code-block:: json

   {
    "metrics":
    [
      {
        "session_h": "e9188c68dd9ddeccd0a2f59422d16a2bf7337683",
        "context_h": "0041724ff4e0adac62b70b4f810c79fc5ad8ba5b",
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
        "session_h": "e9188c68dd9ddeccd0a2f59422d16a2bf7337683",
        "context_h": "0041724ff4e0adac62b70b4f810c79fc5ad8ba5b",
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

Count metrics of a context
--------------------------
Count all metrics linked to the specified context.

    GET /api/v1/contexts/:context/metrics/count/

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| context       | string   | Yes      | Full context identification key.        |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/contexts/0041724ff4e0adac62b70b4f810c79fc5ad8ba5b/

Example response:

.. code-block:: json

   {
     "count": 1200
   }

Get context details
-------------------
List all contexts which have same identification key prefix.

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| context       | string   | Yes      | Context identification key.             |
+---------------+----------+----------+-----------------------------------------+
| page          | integer  | No       | Directly jump to the requested page.    |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/contexts/0041724ff4e0

Example response:

.. code-block:: json

   {
    "contexts":
     [
      {
        "h": "0041724ff4e0adac62b70b4f810c79fc5ad8ba5b",
        "cpu_count": 8,
        "cpu_frequency": 2500,
        "cpu_type": "i386",
        "cpu_vendor": "",
        "ram_total": 16384,
        "machine_node": "host.name.org",
        "machine_type": "x86_64",
        "machine_arch": "64bit",
        "system_info": "Linux - 3.10.0-693.el7.x86_64",
        "python_info": "3.6.10 packaged by conda-forge"
      },
      {
        "h": "0041724ff4e0e9188c68dd9ddeccd0a2f59422d1",
        "cpu_count": 80,
        "cpu_frequency": 3200,
        "cpu_type": "i586",
        "cpu_vendor": "",
        "ram_total": 262144,
        "machine_node": "host8.name.org",
        "machine_type": "x86_64",
        "machine_arch": "64bit",
        "system_info": "Linux - 3.10.0-693.el7.x86_64",
        "python_info": "3.8.1 packaged by conda-forge"
      }
     ],
    "prev_url": "/api/v1/contexts/?page=1",
    "next_url": "/api/v1/contexts/?page=3",
    "total_page": 3
   }
