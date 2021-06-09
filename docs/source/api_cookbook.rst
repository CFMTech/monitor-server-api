.. SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
..
.. SPDX-License-Identifier: MIT

========
Cookbook
========

Extending Metrics with Sessions information
-------------------------------------------

Objective
    Read all metrics of a session identifier (SID) and export to pandas Dataframe
    indexed on the session run date. We want to restrict the export with the following entries:

    - item name,
    - item variant,
    - memory usage,
    - run date
    - source code reference.

.. code-block:: python

    from monitor_api import Monitor, Sessions, Field, Metrics
    from datetime import datetime

    FIELDS = [Field.ITEM, Field.ITEM_VARIANT, Field.MEM_USAGE, Field.RUN_DATE, Field.SCM]
    SID = '3bb11505e8cb7354fe0af2221c8f6db560fbb2de'
    URL = 'https://my.monitor.org/'
    mon = Monitor(URL)

    sessions = Sessions()
    sessions[SID] = mon.get_session(SID)
    metrics = mon.list_session_metrics(SID)

    df = metrics.to_df(session, keep=FIELDS).set_index(Field.RUN_DATE, inplace=True)


Collecting Sessions with specific tags
--------------------------------------

Objective
    During your monitoring phase, you positioned a description tag named 'my_tag' and another tag called
    'numpy' which contains the numpy version. You want to read all sessions from the remote servers that:

    - has the tag 'my_tag' set.
    - then restrict all sessions known by the server to the ones having tags 'numpy' positioned to "118"
      and 'my_tag' to any value.

.. code-block:: python

    from monitor_api import Monitor, Session

    URL = 'https://my.monitor.org/'
    mon = Monitor(URL)

    sessions_with_my_tag = mon.list_sessions(with_tags=['my_tag'])
    sessions_with_my_tag_and_numpy_118 = mon.list_sessions(with_tags=['my_tag'],
                                                           restrict_flags=dict(numpy="118")
                                                           method="match_all")

Implement a custom validator
----------------------------

Objective
    You want to read all sessions referenced by the server, but you do not want sessions before a given
    reference date which are useless for your analysis.


.. code-block:: python

    from monitor_api import Monitor, Session
    from datetime import datetime

    URL = 'https://my.monitor.org/'
    REF_DATE = datetime(2021, 1, 1)

    def check_date_after_REF_DATE(data: Session) -> Boolean:
        return data.start_date > REF_DATE

    mon = Monitor(URL)
    all_sessions = mon.list_sessions()
    sessions_after_REF_DATE = all_sessions.filter_with(check_date_after_REF_DATE)


Retrieve metrics from last 3 build of a pipeline
------------------------------------------------

Objective
    Running a pipeline 'master' with incremental build number.
    You want metrics from last 3 builds of this pipeline
    concerning the test function 'test_that' for which there is no parametrization.

.. code-block:: python

    from monitor_api import Monitor, Metrics, Sessions

    URL = 'https://my.monitor.org/'
    PIPELINE = 'master'

    def keep_only_test_that(m):
        return m.item == 'test_that'

    mon = Monitor(URL)
    last_3_builds = sorted(mon.list_pipeline_builds(PIPELINE), reverse=True)[:-3]
    metrics = Metrics()
    for build in last_3_builds:
        sessions = mon.list_build_sessions(PIPELINE, build)
        m = mon.list_session_metrics(sessions).filter_with(keep_only_test_that)
        metrics = metrics.merge(m)
    print(len(metrics))

Sending local database to a monitor-server
------------------------------------------

Objective
    You have a local database with different measures. You want to send them to your server
    without rerunning tests.

