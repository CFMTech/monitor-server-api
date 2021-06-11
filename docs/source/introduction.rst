.. SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
..
.. SPDX-License-Identifier: MIT

============
Introduction
============

Thanks to `pytest-monitor <https://pytest-monitor.readthedocs.io/en/latest/>`_, you can check for resource consumption of your tests written using `pytest
<http://pytest.org/>`_.
However, experience in analyzing collected data turned out to be tedious:

 - it often requires specific code and queries to fetch the data
 - focusing on specific features requires specific processing
 - `pytest-monitor <https://pytest-monitor.readthedocs.io/en/latest/>`_ does not support parallelism.

These are the main reasons why the `monitor-server-api` has been written. The `monitor-server-api` provides
two components:

- the `monitor-server`: a REST server for storing and fetching data

.. code-block:: shell

    $> # Send pytest-monitor analysis to a monitor-server
    $> pytest --remote http://monitor.instance.org:8181

- the `monitor-api`: an API designed to easily query and filter data either from either

    * a `monitor-server` through the provided REST api
    * a local `pytest-monitor <https://pytest-monitor.readthedocs.io/en/latest/>`_ database.

.. code-block:: python

    import monitor as my

    # Connect to remote server
    srv = my.Monitor('https://somewhere.org', verify=True)
    # Get all sessions with both conditions met
    #  - python set as a tag (regardless of its value)
    #  - pandas tag set to value 1.0.1
    with srv.read_sessions(with_tags=['python', 'pandas'], restrict_flags=['3.6', '1.0.5']) as sessions:
        # Retrieve metrics
        my_metrics = srv.get_metrics_from(sessions=sessions)
    # Dump them as pandas DataFrame
    print(my_metrics.to_df(keep=[my.COMPONENT, my.ITEM, my.KERNEL_TIME]).set_index(my.ITEM))

