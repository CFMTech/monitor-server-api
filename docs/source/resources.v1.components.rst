.. SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
..
.. SPDX-License-Identifier: MIT

List components
---------------
List all components for which at least one metric is associated.

    GET /api/v1/components/:component_prefix/

Parameters
~~~~~~~~~~
+------------------+----------+----------+-----------------------------------------+
| Attribute        | Type     | Required |  Description                            |
+==================+==========+==========+=========================================+
| component_prefix | string   | No       | Keep only components starting with      |
|                  |          |          | the given prefix.                       |
+------------------+----------+----------+-----------------------------------------+
| page             | integer  | No       | Directly jump to the requested page.    |
+------------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/components/

Example response:

.. code-block:: json

    {
     "components":
      [
       "component_10",
       "component_20"
      ],
     "prev_url": "/api/v1/components/?page=1",
     "next_url": "/api/v1/components/?page=3",
     "total_page": 3
    }

Counting components
-------------------
Count all components, excluding empty entries.

    GET /api/v1/components/count/

Parameters
~~~~~~~~~~
None

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/components/count/

Example response:

.. code-block:: json

    {
       "count": 123
    }

Listing metrics of a component
------------------------------
List all metrics of a given component.

    GET /api/v1/components/:component/metrics/
    GET /api/v1/components/metrics

Parameters
~~~~~~~~~~
+------------------+----------+----------+-----------------------------------------+
| Attribute        | Type     | Required |  Description                            |
+==================+==========+==========+=========================================+
| component        | string   | No       | A valid component. If you wish to       |
|                  |          |          | retrieve metrics which do not have a    |
|                  |          |          | component, leave it blank or use the    |
|                  |          |          | second end point.                       |
+------------------+----------+----------+-----------------------------------------+
| page             | integer  | No       | Directly jump to the requested page.    |
+------------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/components/component_1/metrics

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
        "component": "component_1",
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
        "component": "component_1",
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

List pipelines associated to a component
----------------------------------------
Get all pipelines that collect metrics for the desired component.

    GET /api/v1/components/:component/pipelines/

Parameters
~~~~~~~~~~
+------------------+----------+----------+-----------------------------------------+
| Attribute        | Type     | Required |  Description                            |
+==================+==========+==========+=========================================+
| component        | string   | Yes      | A valid component.                      |
+------------------+----------+----------+-----------------------------------------+
| page             | integer  | No       | Directly jump to the requested page.    |
+------------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/components/component_1/pipelines/

Example response:

.. code-block:: json

   {
     "component": "component_1",
     "pipelines":
      [
       "jenkinsci:monitor",
       "circleci:monitor"
      ],
     "prev_url": "/api/v1/components/component_1/pipelines/?page=1",
     "next_url": "/api/v1/components/component_1/pipelines/?page=3",
     "total_page": 3
   }

List available builds of a pipeline associated to a component
-------------------------------------------------------------
Get all builds id of a pipeline that collects metrics for the desired component.

    GET /api/v1/components/:component/pipelines/:pipeline/builds

Parameters
~~~~~~~~~~
+------------------+----------+----------+-----------------------------------------+
| Attribute        | Type     | Required |  Description                            |
+==================+==========+==========+=========================================+
| component        | string   | Yes      | A valid component.                      |
+------------------+----------+----------+-----------------------------------------+
| pipeline         | string   | Yes      | A valid pipeline identifier.            |
+------------------+----------+----------+-----------------------------------------+
| page             | integer  | No       | Directly jump to the requested page.    |
+------------------+----------+----------+-----------------------------------------+


Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/components/component_1/pipelines/jenkinsci/builds/

Example response:

.. code-block:: json

   {
     "component": "component_1",
     "pipeline": "jenkinsci",
     "builds":
      [
       "Build 1",
       "Build 2"
      ],
     "prev_url": "/api/v1/components/component_1/pipelines/jenkinsci/builds/?page=1",
     "next_url": "/api/v1/components/component_1/pipelines/jenkinsci/builds/?page=3",
     "total_page": 3
   }

List sessions of a build associated to a component
--------------------------------------------------
Get all sessions matching the given build and having metrics with the given component.

    GET /api/v1/components/<string:component>/pipelines/<string:pipeline>/builds/<string:build>/sessions

Parameters
~~~~~~~~~~
+------------------+----------+----------+-----------------------------------------+
| Attribute        | Type     | Required |  Description                            |
+==================+==========+==========+=========================================+
| component        | string   | Yes      | A valid component.                      |
+------------------+----------+----------+-----------------------------------------+
| pipeline         | string   | Yes      | A valid pipeline identifier.            |
+------------------+----------+----------+-----------------------------------------+
| build            | string   | Yes      | A valid build identifier.               |
+------------------+----------+----------+-----------------------------------------+
| page             | integer  | No       | Directly jump to the requested page.    |
+------------------+----------+----------+-----------------------------------------+


Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/components/component_1/pipelines/jenkinsci/builds/30/sessions

Example response:

.. code-block:: json

   {
     "component": "component_1",
     "pipeline": "jenkinsci",
     "build": "30",
     "sessions":
      [
       "de72c6aa0c32b1ff6ba83bbe5d811bba4636c20f",
       "082f21a0d5023c37b5c84400b7e6b3bee6dda003"
      ],
     "prev_url": "/api/v1/components/component_1/pipelines/jenkinsci/builds/30/sessions?page=1",
     "next_url": "/api/v1/components/component_1/pipelines/jenkinsci/builds/30/sessions?page=3",
     "total_page": 3
   }

Listing a component's item metrics
-----------------------------------
List all metrics of a given component.

    GET /api/v1/components/items/<string:item>/metrics
    GET /api/v1/components/<string:component>/items/<string:item>/metrics

Parameters
~~~~~~~~~~
+------------------+----------+----------+-----------------------------------------+
| Attribute        | Type     | Required |  Description                            |
+==================+==========+==========+=========================================+
| component        | string   | No       | A valid component. If you wish to       |
|                  |          |          | retrieve metrics which do not have      |
|                  |          |          | component, leave it blank or use the    |
|                  |          |          | second end point.                       |
+------------------+----------+----------+-----------------------------------------+
| item             | string   | Yes      | A valid test item name.                 |
+------------------+----------+----------+-----------------------------------------+
| page             | integer  | No       | Directly jump to the requested page.    |
+------------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/components/component_1/items/test_my_item/metrics

.. code-block:: json

   {
    "metrics":
    [
      {
        "session_h": "0041724ff4e0adac62b70b4f810c79fc5ad8ba5b",
        "context_h": "e9188c68dd9ddeccd0a2f59422d16a2bf7337683",
        "item_start_time": "2020-12-04T23:18:15.661016",
        "item_path": "tests.test_file",
        "item": "test_my_item",
        "item_variant": "test_my_item[]",
        "item_fs_loc": "tests/test_file.py",
        "kind": "function",
        "component": "component_1",
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
        "item": "test_my_item",
        "item_variant": "test_my_item[]",
        "item_fs_loc": "tests/test_file.py",
        "kind": "function",
        "component": "component_1",
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

Listing a component's variant metrics
-------------------------------------
List all metrics of a given variant located under the specified component.

    GET /api/v1/components/variants/<string:variant>/metrics
    
    GET /api/v1/components/<string:component>/variants/<string:variant>/metrics

Parameters
~~~~~~~~~~
+------------------+----------+----------+-----------------------------------------+
| Attribute        | Type     | Required |  Description                            |
+==================+==========+==========+=========================================+
| component        | string   | No       | A valid component. If you wish to       |
|                  |          |          | retrieve metrics which do not have      |
|                  |          |          | component, leave it blank or use the    |
|                  |          |          | second end point.                       |
+------------------+----------+----------+-----------------------------------------+
| variant          | string   | Yes      | A valid test item variant.              |
+------------------+----------+----------+-----------------------------------------+
| page             | integer  | No       | Directly jump to the requested page.    |
+------------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/components/component_1/variants/test_my_item_variant[]/metrics

.. code-block:: json

   {
    "metrics":
    [
      {
        "session_h": "0041724ff4e0adac62b70b4f810c79fc5ad8ba5b",
        "context_h": "e9188c68dd9ddeccd0a2f59422d16a2bf7337683",
        "item_start_time": "2020-12-04T23:18:15.661016",
        "item_path": "tests.test_file",
        "item": "test_my_item_variant",
        "item_variant": "test_my_item_variant[]",
        "item_fs_loc": "tests/test_file.py",
        "kind": "function",
        "component": "component_1",
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
        "item": "test_my_item_variant",
        "item_variant": "test_my_item_variant[]",
        "item_fs_loc": "tests/test_file.py",
        "kind": "function",
        "component": "component_1",
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