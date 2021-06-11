.. SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
..
.. SPDX-License-Identifier: MIT

==================
REST API resources
==================

.. tip::

    Current level is v1.

Metric resource
---------------
The **metrics** namespace provide entry points for reading and creating metrics entries.
Despite a metric is associated with both an execution context and a session, the `monitor-server` does not require
prior knowledge of these element at the moment you `POST` your metric.
This has been done willingly in order to avoid contention and workflow entanglement.

The following API entry points are available in the metric namespace:

.. toctree::
   :maxdepth: 1

   resources.v1.metrics

Filters resource
----------------
This namespace provides special entry points for retrieving metrics from conditions that might involve test sessions.
Retrieving all metrics matching a given SCM reference is a good example.

The following API entry points are available for this namespace:

.. toctree::
   :maxdepth: 1

   resources.v1.filters

Items resource
--------------
The **items** namespace provides the necessary entry points for accessing metrics given a test name.
The following API entry points are available:

.. toctree::
   :maxdepth: 1

   resources.v1.items

Variants resource
-----------------
The **variants** namespace works like the **items** one, but focus on variant tests, i.e. your fully qualified test
name.
The following API entry points are available:

.. toctree::
   :maxdepth: 1

   resources.v1.variants

Session resource
----------------
The session namespace provide entry points for creating, reading and querying information by sessions.
**Sessions** can be seen as a single `pytest` run.
The following API entry points are available in the session namespace:

.. toctree::
   :maxdepth: 1

   resources.v1.sessions

Execution contexts resource
---------------------------
The context namespace provide entry points for creating, reading and querying information by contexts.
**Execution Contexts** (referred to as `contexts` in the `monitor-server-api`) are information about the system which
operated tests.
The following API entry points are available in the contexts namespace:

.. toctree::
   :maxdepth: 1

   resources.v1.contexts

Components resource
-------------------
**Components** aims is to help you categorize tests. This can be by entity (a library for instance), a specific part in
your core system or anything else. They are useful to restrict your queries.
The following API entry points are available in the components namespace:

.. toctree::
   :maxdepth: 1

   resources.v1.components

Pipelines and build resource
----------------------------
**Pipelines** have been introduced to help comparing results between two changes from a CI point of view.
They are automatically set by `pytest-monitor` on the following Software Factories:

- Jenkins
- GitlabCI
- DroneCI
- TravisCI
- CircleCI

The following API entry points are available in the pipelines namespace:

.. toctree::
   :maxdepth: 1

   resources.v1.pipelines

Resource Usages resource
------------------------
This namespace is all about collecting tests which consumes most (resp. less) a given resource.
You can filter by sub-resource like components or pipelines.

To retrieve these metrics, consider the following entry points:

.. toctree::
   :maxdepth: 1

   resources.v1.resources
