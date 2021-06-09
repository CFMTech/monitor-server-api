# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

def test_pipelines_get(monitor, gen):
    monitor.assert_no_sessions()
    for b in ['circleci:monitor', 'jenkins:monitor', 'droneci:monitor', 'travisci:monitor', 'bamboo:monitor']:
        s = gen.new_session(pipeline_branch=b)
        monitor.post_sessions_v1(s)
    monitor.assert_session_count(5)
    resp = monitor.client.get('/api/v1/pipelines/')
    assert resp.json == dict(pipelines=['circleci:monitor', 'jenkins:monitor', 'droneci:monitor',
                                        'travisci:monitor', 'bamboo:monitor'])


def test_single_pipelines_get(monitor, gen):
    monitor.assert_no_sessions()
    page_1, page_2 = [], []
    for bno in range(1, 11):
        s = gen.new_circleci_session(buildno=str(bno + 987654321))
        if len(page_1) < 5:
            page_1.append(str(987654321 + bno))
        else:
            page_2.append(str(987654321 + bno))
        monitor.post_sessions_v1(s)
    for bno in range(1, 11):
        s = gen.new_jenkins_session(buildno=bno)
        monitor.post_sessions_v1(s)
    monitor.assert_session_count(20)
    tmp = monitor.client.get('/api/v1/pipelines/circleci:monitor/builds').json
    assert tmp == dict(pipeline="circleci:monitor", builds=page_1,
                       next_url='/api/v1/pipelines/circleci:monitor/builds?page=2',
                       prev_url=None,
                       total_page=2)
    tmp = monitor.client.get('/api/v1/pipelines/circleci:monitor/builds?page=2').json
    assert tmp == dict(pipeline="circleci:monitor", builds=page_2,
                       next_url=None,
                       prev_url='/api/v1/pipelines/circleci:monitor/builds?page=1',
                       total_page=2)


def test_single_pipelines_w_multiple_sessions_per_build(monitor, gen):
    monitor.assert_no_sessions()
    page_bno3, page_bno8 = [], []
    for bno in range(1, 11):
        build_number = str(bno + 987654321)
        s1 = gen.new_circleci_session(buildno=build_number)
        s2 = gen.new_circleci_session(buildno=build_number)
        s3 = gen.new_circleci_session(buildno=build_number)
        if bno >= 6:
            monitor.post_sessions_v1(s1, s2, s3)
        else:
            monitor.post_sessions_v1(s1, s2)
        if bno == 2:
            page_bno3.append(s1['session_h'])
            page_bno3.append(s2['session_h'])
        elif bno == 8:
            page_bno8.append(s1['session_h'])
            page_bno8.append(s2['session_h'])
            page_bno8.append(s3['session_h'])
    for bno in range(1, 11):
        s = gen.new_jenkins_session(buildno=bno)
        monitor.post_sessions_v1(s)

    monitor.assert_session_count(35)

    tmp = monitor.client.get('/api/v1/pipelines/circleci:monitor/builds/987654323/sessions').json
    assert tmp == dict(build='987654323', pipeline="circleci:monitor",
                       sessions=page_bno3,
                       next_url=None,
                       prev_url=None,
                       total_page=1)
    tmp = monitor.client.get('/api/v1/pipelines/circleci:monitor/builds/987654329/sessions').json
    assert tmp == dict(build='987654329', pipeline="circleci:monitor",
                       sessions=page_bno8,
                       next_url=None,
                       prev_url=None,
                       total_page=1)


def test_get_sessions_of_component_with_fixed_build(monitor, gen):
    monitor.assert_no_sessions()
    c = gen.new_context()
    monitor.post_contexts_v1(c)
    dico_sessions = dict()
    for bno in range(1, 11):
        build_number = str(bno + 987654321)
        s1 = gen.new_circleci_session(buildno=build_number)
        s2 = gen.new_circleci_session(buildno=build_number)
        s3 = gen.new_circleci_session(buildno=build_number)
        if build_number == '987654329':
            dico_sessions["s2"] = s2
            dico_sessions["s3"] = s3
        monitor.post_sessions_v1(s1, s2, s3)
        for component, session in zip(['compA', 'compB', 'compC'], [s1, s2, s3]):
            for count in range(10):
                m = gen.new_metric(c, session, component=component)
                monitor.post_metrics_v1(m)
        else:
            if build_number == '987654329':
                # We add one metric for session s3 on compB
                m = gen.new_metric(c, s3, component="compB")
                monitor.post_metrics_v1(m)

    monitor.assert_session_count(30)
    monitor.assert_metric_count(301)
    r = monitor.client.get('/api/v1/components/compB/pipelines/circleci:monitor/builds/987654329/sessions').json
    assert r == dict(component='compB', pipeline='circleci:monitor', build='987654329',
                     sessions=[dico_sessions["s2"]['session_h'], dico_sessions["s3"]['session_h']],
                     next_url=None, prev_url=None, total_page=1)
