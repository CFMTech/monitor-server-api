.. SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
..
.. SPDX-License-Identifier: MIT

========
REST API
========

The `monitor-server` provides a REST API which comply with `OpenAPI Specification (OAS) <https://swagger.io/specification/>`_.
The documentation is readily accessible on a per version basis for each API version provided by the server.

Current status of the `monitor-server` relies on api v1. No other version of the API is provided for now.

Basic usage
-----------
API requests should be prefixed with both api and the API version. For example, the root of the v1 API is at /api/v1.
The following sections illustrate different uses:

If you have a `monitor-server` instance at monitor.example.org:

.. code-block:: bash

    $ curl "https://monitor.example.org/api/v1/metrics"

The API uses JSON to serialize data. You don’t need to specify .json at the end of an API URL.

Status code
-----------
The API is designed to return different status codes according to context and action.
This way, if a request results in an error, the caller is able to get insight into what went wrong.
The following table gives an overview of how the API functions behave:

+--------------+-------------------------+----------------------------------------------------+
| Request type | Return code             | Description                                        |
+==============+=========================+====================================================+
|              | `Return 200 OK`         | The resource exists and has been accessed.         |
| GET          +-------------------------+----------------------------------------------------+
|              | `Return 404 Not Found`  | The resource does not exists or cannot be accessed.|
+--------------+-------------------------+----------------------------------------------------+
| POST         | `Return 201 Created`    | The resource has been successfully created and is  |
|              |                         | returned as JSON                                   |
+--------------+-------------------------+----------------------------------------------------+

.. note::

    At the moment, `PUT`, `DELETE` and `PATCH` are not supported.

Pagination
----------
Sometimes, the returned result is too large to be sent in a single response. To solve this problem, the `monitor-server`
support Offset-based pagination. This is the default method and it is available on nearly all endpoints.
When listing resources, you can pass the `page` parameter to directly jump to the desired page:

.. code-block:: bash

    $ curl "https://monitor.example.org/api/v1/metrics?page=3"

The following semantic is supported for the page parameter:

 - if `page` is provided as a positive number, the page whose index matches the requested value is returned
 - if `page` is given as a negative number, then, negative index is used, meaning that pages are indexed from the end.

An example is worth a thousand words.

.. code-block:: bash

    $ # Returns page number 3
    $ curl "https://monitor.example.org/api/v1/metrics?page=3"
    $ # Returns last page
    $ curl "https://monitor.example.org/api/v1/metrics?page=-1"
    $ # Returns before before last page
    $ curl "https://monitor.example.org/api/v1/metrics?page=-3"
