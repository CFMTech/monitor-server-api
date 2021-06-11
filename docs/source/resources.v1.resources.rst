.. SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
..
.. SPDX-License-Identifier: MIT

List metrics with highest/lowest resource usage
-----------------------------------------------
Retrieve all metrics having the highest or lowest consumption of the desired resource across all your data set.
Queryable resources are:

- memory
- cpu
- kernel_time
- user_time
- total_time

This entry point limits to 500 the number of listed elements.

    GET /api/v1/resources/<string:resource>/head/metrics

    GET /api/v1/resources/<string:resource>/head/<int:max_element>/metrics
    
    GET /api/v1/resources/<string:resource>/tail/metrics
    
    GET /api/v1/resources/<string:resource>/tail/<int:max_element>/metrics

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| resource      | string   | Yes      | The type of resource.                   |
+---------------+----------+----------+-----------------------------------------+
| max_element   | int      | No       | Maximum number of element to retrieve.  |
+---------------+----------+----------+-----------------------------------------+
| page          | integer  | No       | Directly jump to the requested page.    |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/resources/cpu/head/5/metrics

Example response:

.. code-block:: json

  {
   "metrics": [
     {
       "session_h": "c9dd28cd8bb77f420a00dd229cc87f53",
       "context_h": "9ae6c23d7c6b4562393385edf6da8500",
       "item_start_time": "2021-02-09T11:41:35.990018",
       "item_path": "test_prime",
       "item": "test_prime",
       "item_variant": "test_prime[982451653]",
       "item_fs_loc": "tests/test_prime.py",
       "kind": "function",
       "component": "component",
       "total_time": 0.009404897689819336,
       "user_time":  0.002093055999999982,
       "kernel_time": 0.004456143999999995,
       "cpu_usage": 0.9,
       "mem_usage": 12538
     },
     {
       "session_h": "c9dd28cd8bb77f420a00dd229cc87f53",
       "context_h": "9ae6c23d7c6b4562393385edf6da8500",
       "item_start_time": "2021-02-09T11:41:36.003282",
       "item_path": "test_prime",
       "item": "test_prime",
       "item_fs_loc": "tests/test_prime.py",
       "component": "component",
       "item_variant": "test_prime[982451653]",
       "kind": "function",
       "total_time": 0.8004801273345947,
       "user_time": 0.722636224,
       "kernel_time": 0.069095616,
       "cpu_usage": 0.8,
       "mem_usage": 12334
     },
     {
       "session_h": "c9dd28cd8bb77f420a00dd229cc87f53",
       "context_h": "9ae6c23d7c6b4562393385edf6da8500",
       "item_start_time": "2021-02-09T11:41:36.809390",
       "item_path": "test_prime",
       "item": "test_prime",
       "item_fs_loc": "tests/test_prime.py",
       "item_variant": "test_prime[982451653]",
       "component": "component",
       "kind": "function",
       "total_time": 678.7139070034027,
       "user_time": 676.4789990400001,
       "kernel_time": 1.144489664,
       "cpu_usage": 0.7,
       "mem_usage": 11774
     }
   ],
   "next_url": "/resources/cpu/head/5/metrics/?page=2",
   "total_page": 2
  }

List all metrics with highest/lowest resource usage on a specific component
---------------------------------------------------------------------------
Retrieve all metrics having the highest or lowest consumption of the desired resource for all metrics with the
specified component.
Queryable resources are:

- memory
- cpu
- kernel_time
- user_time
- total_time

This entry point limits to 500 the number of listed elements.

    GET /api/v1/resources/<string:resource>/components/<string:component>/head/<int:max_element>/metrics

    GET /api/v1/resources/<string:resource>/components/<string:component>/head/metrics
    
    GET /api/v1/resources/<string:resource>/components/<string:component>/tail/<int:max_element>/metrics
    
    GET /api/v1/resources/<string:resource>/components/<string:component>/tail/metrics

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| resource      | string   | Yes      | The type of resource.                   |
+---------------+----------+----------+-----------------------------------------+
| component     | string   | Yes      | The component to use for filtering.     |
+---------------+----------+----------+-----------------------------------------+
| max_element   | int      | No       | Maximum number of element to retrieve.  |
+---------------+----------+----------+-----------------------------------------+
| page          | integer  | No       | Directly jump to the requested page.    |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/resources/cpu/components/component_1/head/5/metrics

Example response:

.. code-block:: json

  {
   "metrics": [
     {
       "session_h": "c9dd28cd8bb77f420a00dd229cc87f53",
       "context_h": "9ae6c23d7c6b4562393385edf6da8500",
       "item_start_time": "2021-02-09T11:41:35.990018",
       "item_path": "test_prime",
       "item": "test_prime",
       "item_variant": "test_prime[982451653]",
       "item_fs_loc": "tests/test_prime.py",
       "kind": "function",
       "component": "component_1",
       "total_time": 0.009404897689819336,
       "user_time":  0.002093055999999982,
       "kernel_time": 0.004456143999999995,
       "cpu_usage": 0.9,
       "mem_usage": 12538
     },
     {
       "session_h": "c9dd28cd8bb77f420a00dd229cc87f53",
       "context_h": "9ae6c23d7c6b4562393385edf6da8500",
       "item_start_time": "2021-02-09T11:41:36.003282",
       "item_path": "test_prime",
       "item": "test_prime",
       "item_fs_loc": "tests/test_prime.py",
       "component": "component_1",
       "item_variant": "test_prime[982451653]",
       "kind": "function",
       "total_time": 0.8004801273345947,
       "user_time": 0.722636224,
       "kernel_time": 0.069095616,
       "cpu_usage": 0.8,
       "mem_usage": 12334
     },
     {
       "session_h": "c9dd28cd8bb77f420a00dd229cc87f53",
       "context_h": "9ae6c23d7c6b4562393385edf6da8500",
       "item_start_time": "2021-02-09T11:41:36.809390",
       "item_path": "test_prime",
       "item": "test_prime",
       "item_fs_loc": "tests/test_prime.py",
       "item_variant": "test_prime[982451653]",
       "component": "component_1",
       "kind": "function",
       "total_time": 678.7139070034027,
       "user_time": 676.4789990400001,
       "kernel_time": 1.144489664,
       "cpu_usage": 0.7,
       "mem_usage": 11774
     }
   ],
   "next_url": "/resources/cpu/pipelines/classic/head/5/metrics/?page=2",
   "total_page": 2
  }

List all metrics with highest/lowest resource usage on a specific pipeline
--------------------------------------------------------------------------
Retrieve all metrics having the highest or lowest consumption of the desired resource for all metrics linked to the
given pipeline.
Queryable resources are:

- memory
- cpu
- kernel_time
- user_time
- total_time

This entry point limits to 500 the number of listed elements.

    GET /api/v1/resources/<string:resource>/pipelines/<string:pipeline>/head/<int:max_element>/metrics
    
    GET /api/v1/resources/<string:resource>/pipelines/<string:pipeline>/head/metrics
    
    GET /api/v1/resources/<string:resource>/pipelines/<string:pipeline>/tail/<int:max_element>/metrics
    
    GET /api/v1/resources/<string:resource>/pipelines/<string:pipeline>/tail/metrics

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| resource      | string   | Yes      | The type of resource.                   |
+---------------+----------+----------+-----------------------------------------+
| pipeline      | string   | Yes      | The pipeline name to use for filtering. |
+---------------+----------+----------+-----------------------------------------+
| max_element   | int      | No       | Maximum number of element to retrieve.  |
+---------------+----------+----------+-----------------------------------------+
| page          | integer  | No       | Directly jump to the requested page.    |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/resources/cpu/pipelines/classic/head/5/metrics

Example response:

.. code-block:: json

  {
   "metrics": [
     {
       "session_h": "c9dd28cd8bb77f420a00dd229cc87f53",
       "context_h": "9ae6c23d7c6b4562393385edf6da8500",
       "item_start_time": "2021-02-09T11:41:35.990018",
       "item_path": "test_prime",
       "item": "test_prime",
       "item_variant": "test_prime[982451653]",
       "item_fs_loc": "tests/test_prime.py",
       "kind": "function",
       "component": "component_1",
       "total_time": 0.009404897689819336,
       "user_time":  0.002093055999999982,
       "kernel_time": 0.004456143999999995,
       "cpu_usage": 0.9,
       "mem_usage": 12538
     },
     {
       "session_h": "c9dd28cd8bb77f420a00dd229cc87f53",
       "context_h": "9ae6c23d7c6b4562393385edf6da8500",
       "item_start_time": "2021-02-09T11:41:36.003282",
       "item_path": "test_prime",
       "item": "test_prime",
       "item_fs_loc": "tests/test_prime.py",
       "component": "component_1",
       "item_variant": "test_prime[982451653]",
       "kind": "function",
       "total_time": 0.8004801273345947,
       "user_time": 0.722636224,
       "kernel_time": 0.069095616,
       "cpu_usage": 0.8,
       "mem_usage": 12334
     },
     {
       "session_h": "c9dd28cd8bb77f420a00dd229cc87f53",
       "context_h": "9ae6c23d7c6b4562393385edf6da8500",
       "item_start_time": "2021-02-09T11:41:36.809390",
       "item_path": "test_prime",
       "item": "test_prime",
       "item_fs_loc": "tests/test_prime.py",
       "item_variant": "test_prime[982451653]",
       "component": "component_1",
       "kind": "function",
       "total_time": 678.7139070034027,
       "user_time": 676.4789990400001,
       "kernel_time": 1.144489664,
       "cpu_usage": 0.7,
       "mem_usage": 11774
     }
   ],
   "next_url": "/resources/cpu/components/component_1/head/5/metrics/?page=2",
   "total_page": 2
  }

List all metrics with highest/lowest resource usage on a specific build
-----------------------------------------------------------------------
Retrieve all metrics having the highest or lowest consumption of the desired resource for all metrics linked
to the specified build.
Queryable resources are:

- memory
- cpu
- kernel_time
- user_time
- total_time

This entry point limits to 500 the number of listed elements.

    GET /api/v1/resources/<string:resource>/pipelines/<string:pipeline>/builds/<string:build>/head/<int:max_element>/metrics
    
    GET /api/v1/resources/<string:resource>/pipelines/<string:pipeline>/builds/<string:build>/head/metrics
    
    GET /api/v1/resources/<string:resource>/pipelines/<string:pipeline>/builds/<string:build>/tail/<int:max_element>/metrics
    
    GET /api/v1/resources/<string:resource>/pipelines/<string:pipeline>/builds/<string:build>/tail/metrics


Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| resource      | string   | Yes      | The type of resource.                   |
+---------------+----------+----------+-----------------------------------------+
| pipeline      | string   | Yes      | The pipeline name to use for filtering. |
+---------------+----------+----------+-----------------------------------------+
| build         | string   | Yes      | The build name that will be used to     |
|               |          |          | restrict the search.                    |
+---------------+----------+----------+-----------------------------------------+
| max_element   | int      | No       | Maximum number of element to retrieve.  |
+---------------+----------+----------+-----------------------------------------+
| page          | integer  | No       | Directly jump to the requested page.    |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/resources/cpu/pipelines/classic/builds/314/head/5/metrics

Example response:

.. code-block:: json

  {
   "metrics": [
     {
       "session_h": "c9dd28cd8bb77f420a00dd229cc87f53",
       "context_h": "9ae6c23d7c6b4562393385edf6da8500",
       "item_start_time": "2021-02-09T11:41:35.990018",
       "item_path": "test_prime",
       "item": "test_prime",
       "item_variant": "test_prime[982451653]",
       "item_fs_loc": "tests/test_prime.py",
       "kind": "function",
       "component": "component_1",
       "total_time": 0.009404897689819336,
       "user_time":  0.002093055999999982,
       "kernel_time": 0.004456143999999995,
       "cpu_usage": 0.9,
       "mem_usage": 12538
     },
     {
       "session_h": "c9dd28cd8bb77f420a00dd229cc87f53",
       "context_h": "9ae6c23d7c6b4562393385edf6da8500",
       "item_start_time": "2021-02-09T11:41:36.003282",
       "item_path": "test_prime",
       "item": "test_prime",
       "item_fs_loc": "tests/test_prime.py",
       "component": "component_1",
       "item_variant": "test_prime[982451653]",
       "kind": "function",
       "total_time": 0.8004801273345947,
       "user_time": 0.722636224,
       "kernel_time": 0.069095616,
       "cpu_usage": 0.8,
       "mem_usage": 12334
     },
     {
       "session_h": "c9dd28cd8bb77f420a00dd229cc87f53",
       "context_h": "9ae6c23d7c6b4562393385edf6da8500",
       "item_start_time": "2021-02-09T11:41:36.809390",
       "item_path": "test_prime",
       "item": "test_prime",
       "item_fs_loc": "tests/test_prime.py",
       "item_variant": "test_prime[982451653]",
       "component": "component_1",
       "kind": "function",
       "total_time": 678.7139070034027,
       "user_time": 676.4789990400001,
       "kernel_time": 1.144489664,
       "cpu_usage": 0.7,
       "mem_usage": 11774
     }
   ],
   "next_url": "/resources/cpu/components/component_1/head/5/metrics/?page=2",
   "total_page": 2
  }