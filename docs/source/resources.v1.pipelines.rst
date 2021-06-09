.. SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
..
.. SPDX-License-Identifier: MIT

List pipelines
--------------
Retrieve all available pipelines identifiers.

    GET /api/v1/pipelines/

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

    $ curl -X GET https://monitor.instance.org/api/v1/pipelines/

Example response:

.. code-block:: json

   {
     "pipelines":
      [
       "jenkinsci:monitor",
       "circleci:monitor"
      ],
     "prev_url": "/api/v1/components/component_1/pipelines/?page=1",
     "next_url": "/api/v1/components/component_1/pipelines/?page=3",
     "total_page": 3
   }


List builds of a pipeline
-------------------------
Retrieve all available builds for a single pipeline identifier.

    GET /api/v1/pipelines/:pipeline/builds

Parameters
~~~~~~~~~~
+---------------+----------+----------+-----------------------------------------+
| Attribute     | Type     | Required |  Description                            |
+===============+==========+==========+=========================================+
| pipeline      | string   | Yes      | A valid pipeline identifier.            |
+---------------+----------+----------+-----------------------------------------+
| page          | integer  | No       | Directly jump to the requested page.    |
+---------------+----------+----------+-----------------------------------------+

Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/pipelines/jenkinsci/builds

Example response:

.. code-block:: json

   {
    "pipeline": "jenkinsci",
    "builds":
     [
      {
       "id": "Build 1",
       "sessions":
        [
         "3bb11505e8cb7354fe0af2221c8f6db560fbb2de",
         "c8f2d7bbbbd0fb2b8ddaad9938ad13281380c73e"
        ]
      },
      {
       "id": "Build 2",
       "sessions":
        [
         "ef53a92b28f2e55ab3b26f8db6adcf899dd33503"
        ]
      }
     ],
    "prev_url": "/api/v1/components/component_1/pipelines/jenkinsci/builds/?page=1",
    "next_url": "/api/v1/components/component_1/pipelines/jenkinsci/builds/?page=3",
    "total_page": 3
   }

List all build sessions
-----------------------
Get all sessions linked to the given build (pipeline, build ref).

    GET /api/v1/pipelines/<string:pipeline>/builds/<string:build>/sessions

Parameters
~~~~~~~~~~
+------------------+----------+----------+-----------------------------------------+
| Attribute        | Type     | Required |  Description                            |
+==================+==========+==========+=========================================+
| pipeline         | string   | Yes      | A valid pipeline identifier.            |
+------------------+----------+----------+-----------------------------------------+
| build            | string   | Yes      | A valid build identifier.               |
+------------------+----------+----------+-----------------------------------------+
| page             | integer  | No       | Directly jump to the requested page.    |
+------------------+----------+----------+-----------------------------------------+


Example
~~~~~~~
.. code-block:: bash

    $ curl -X GET https://monitor.instance.org/api/v1/pipelines/jenkinsci/builds/30/sessions

Example response:

.. code-block:: json

   {
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
