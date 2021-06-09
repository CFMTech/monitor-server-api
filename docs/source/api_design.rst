.. SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
..
.. SPDX-License-Identifier: MIT

==================
Elements of Design
==================

The data model used by *pytest-monitor*, though simple, can quickly become a real challenge to analyze.
Moreover, users wanting to quickly extract their monitoring results can face unwanted complexity when it comes to
analyze the data.

For this reason, an utility library has been written whose purposes are:

- to ease the way data are extracted and presented
- to provide resource oriented entry points so that you can focus on your monitoring

The API design follows these ideas. The following section describe some of the components
used in the API and is intended for guidance and development rather than direct exploitation.
If you want to quickly exploit your metrics, you should head over to the :ref:`monitor` page.

Global overview
---------------
The `monitor api` can be split into 3 main parts:

- one interaction layer which we will refer to as the **dialect** layer.
- the **core entities** layer which provides base objects for accessing collected values.
- the **core collections** layer, whose purpose is to provide pandas conversion and
  raw containers of **core entities** objects.


Monitor Dialects
~~~~~~~~~~~~~~~~
We call dialect the object in charge of extracting metrics, sessions and contexts from a storage such as a local
database or a remote server.

As such, we provide an interface which lists all methods a valid implementation must provide.
The `monitor api` is shipped with two dialects:

- The **Local** dialect which is preferred for interacting with local `sqlite3` database.
- The **Remote** dialect which is preferred for retrieving data from a `monitor-server`.

Entities
~~~~~~~~
Part of the `monitor_api.core` package, entities can be seen as simple object representing rows of the data model
used by `pytest-monitor`. There are currently 3 of them:

- `monitor_api.core.entities.Session` allows you to easily deals with all of the aspects of a test session
- `monitor_api.core.entities.Context` maps all of the machine information used when running tests
- `monitor_api.core.entities.Metric` deals with all collected metrics

Collections
~~~~~~~~~~~
Collections are also part of the `monitor_api.core` package and provide
entities aggregation and export facilities (pandas, file ...):

- `monitor_api.core.collections.Sessions` aggregates `monitor_api.core.entities.Session` using the session key
- `monitor_api.core.collections.Contexts` clusters `monitor_api.core.entities.Context` using their hash key
- `monitor_api.core.collections.Metrics` lists `monitor_api.core.entities.Metric` without condition.

General usage
-------------
Basically, the `monitor_api.Monitor` object will allow you to easily access `monitor_api.core.collections`
objects and `monitor_api.core.entities` ones like `monitor_api.core.entities.Session`
and `monitor_api.core.Context`. In turn, `monitor_api.core.collections` will allow you to access each
`monitor_api.core.entities` individually.

Here under follows a basic example where we list all metrics for a given SCM value:

.. code-block::

    from monitor_api import Monitor

    # Create the monitor
    mon = Monitor('https://my.monitor.server.org')
    # Retrieves a collection
    metrics = mon.list_metrics_by_scm_id('deadbeef')
    # Manipulate entities through collection.
    print(metrics[0].item)
    print(metrics[0].memory_usage)
    # Access a session
    session = mon.get_session(metrics[0].session_h)


