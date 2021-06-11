# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from http import HTTPStatus


def compare_session(remote, expect):
    assert remote['session_h'] == expect['session_h']
    assert remote['run_date'] == expect['run_date']
    assert remote['scm_ref'] == expect['scm_ref']
    assert len(remote['tags']) == len(expect['description'])
    for tag in remote['tags']:
        assert tag['name'] in expect['description']
        assert tag['value'] == expect['description'][tag['name']]


def tests_session_get(monitor, gen):
    monitor.assert_no_sessions()
    s = gen.new_session(scm_ref='deadmeet')
    monitor.post_sessions_v1(s)
    r = monitor.client.get('/api/v1/sessions/')
    assert r.status_code == HTTPStatus.OK
    compare_session(remote=r.json['sessions'][0], expect=s)


def test_sessions_post_bad_description_format(client, gen):
    s = gen.new_session()
    s['description'] = ['bc', 'def']
    r = client.post('/api/v1/sessions/', json=s)
    assert r.status_code == HTTPStatus.BAD_REQUEST


def tests_session_post(client, gen):
    s = gen.new_session()
    r = client.post('/api/v1/sessions/', json=s)
    assert r.status_code == HTTPStatus.CREATED
    compare_session(remote=r.json, expect=s)
    r = client.get('/api/v1/sessions/count')
    assert r.status_code == HTTPStatus.OK
    assert r.json == dict(count=1)


def test_session_filter(monitor, gen):
    s1 = gen.new_session(session_h='deadmeet')
    s2 = gen.new_session(session_h='deadbeef')
    s3 = gen.new_session(session_h='badcoffee')
    monitor.post_sessions_v1(s1, s2, s3)
    r = monitor.client.get('/api/v1/sessions/dead')
    assert r.status_code == HTTPStatus.OK
    assert 'next_url' not in r.json
    assert 'prev_url' not in r.json
    assert len(r.json['sessions']) == 2
    for session in r.json['sessions']:
        if session['session_h'] == s1['session_h']:
            compare_session(remote=session, expect=s1)
        else:
            compare_session(remote=session, expect=s2)
    r = monitor.client.get('/api/v1/sessions/foo')
    assert r.status_code == HTTPStatus.NO_CONTENT


def test_session_match_any_restriction(monitor, gen):
    s1 = gen.new_session(session_h='deadmeet')
    s2 = gen.new_session(session_h='deadbeef', description=dict(wanted_flags="some"))
    s3 = gen.new_session(session_h='badcoffee', description=dict(some_flags="value"))
    monitor.post_sessions_v1(s1, s2, s3)
    r = monitor.client.get('/api/v1/sessions/?method=match_any&with_flags=wanted_flags,some_flags&restrict_flags=some')
    assert len(r.json['sessions']) == 2
    compare_session(remote=r.json['sessions'][0], expect=s2)
    compare_session(remote=r.json['sessions'][1], expect=s3)


def test_session_match_default_restriction(monitor, gen):
    s1 = gen.new_session(session_h='deadmeet')
    s2 = gen.new_session(session_h='deadbeef', description=dict(wanted_flags="some"))
    s3 = gen.new_session(session_h='badcoffee', description=dict(some_flags="value"))
    monitor.post_sessions_v1(s1, s2, s3)
    r = monitor.client.get('/api/v1/sessions/?with_flags=wanted_flags,some_flags&restrict_flags=some')
    assert len(r.json['sessions']) == 2
    compare_session(remote=r.json['sessions'][0], expect=s2)
    compare_session(remote=r.json['sessions'][1], expect=s3)


def test_session_match_all_restriction(monitor, gen):
    s1 = gen.new_session(session_h='deadmeet')
    s2 = gen.new_session(session_h='deadbeef', description=dict(wanted_flags="some"))
    s3 = gen.new_session(session_h='badcoffee', description=dict(some_flags="value"))
    monitor.post_sessions_v1(s1, s2, s3)
    url = '/api/v1/sessions/?method=match_all&with_flags=wanted_flags,pipeline_branch&restrict_flags=some'
    r = monitor.client.get(url)
    assert len(r.json['sessions']) == 1
    compare_session(remote=r.json['sessions'][0], expect=s2)


def test_session_by_scm(monitor, gen):
    xpct_session = set()
    for i in range(10):
        scm = f'deadbeef{i}'
        for j in range(i):
            s = gen.new_session(scm_ref=scm)
            if i == 5:
                xpct_session.add(s['session_h'])
            monitor.post_sessions_v1(s)
    url = '/api/v1/filters/scm/deadbeef5/sessions'
    r = monitor.client.get(url)
    assert len(r.json['sessions']) == 5
    sessions = [s['session_h'] for s in r.json['sessions']]
    for session in xpct_session:
        assert session in sessions
