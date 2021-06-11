# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from http import HTTPStatus
from monitor_server import SERVER
import json


def test_index(monitor, gen):
    c = gen.new_context()
    monitor.post_contexts_v1(c)
    s1, s2, s3 = gen.new_session(), gen.new_session(), gen.new_session()
    for s in (s1, s2, s3):
        monitor.post_sessions_v1(s)
        for i in range(100):
            m = gen.new_metric(c, s)
            monitor.post_metrics_v1(m)
    index = monitor.client.get('/index.html')
    assert index.status_code == HTTPStatus.OK
    # Strip parts, and remove '</p>' at the end
    tmp = index.data.decode().split('\n')
    s = ' '.join([i.strip() for i in index.data.decode().split('\n')[100:115]])[:-4]
    assert '>300<' in s
    assert '>3<' in s
    assert '>1<' in s


def test_pager_get_last(monitor, gen):
    c = gen.new_context()
    monitor.post_contexts_v1(c)
    s1, s2, s3 = gen.new_session(), gen.new_session(), gen.new_session()
    for s in (s1, s2, s3):
        monitor.post_sessions_v1(s)
        for i in range(100):
            m = gen.new_metric(c, s)
            monitor.post_metrics_v1(m)
    resp = monitor.client.get('/api/v1/metrics/?page=-1')
    assert resp.status_code == HTTPStatus.OK
    assert 'next_url' not in resp.json
    assert 'prev_url' in resp.json
    resp = monitor.client.get('/api/v1/metrics/', json=dict(page=-1))
    assert resp.status_code == HTTPStatus.OK
    assert 'next_url' not in resp.json
    assert 'prev_url' in resp.json


def test_pager_page_info(monitor, gen):
    c = gen.new_context()
    monitor.post_contexts_v1(c)
    s1, s2, s3 = gen.new_session(), gen.new_session(), gen.new_session()
    for s in (s1, s2, s3):
        monitor.post_sessions_v1(s)
        for i in range(100):
            m = gen.new_metric(c, s)
            monitor.post_metrics_v1(m)
    resp = monitor.client.get('/api/v1/metrics/?page=-1')
    assert resp.status_code == HTTPStatus.OK
    assert 'next_url' not in resp.json
    assert 'prev_url' in resp.json
    resp = monitor.client.get('/api/v1/metrics/?page=-2')
    assert resp.status_code == HTTPStatus.OK
    assert 'next_url' in resp.json
    assert 'prev_url' in resp.json
    resp = monitor.client.get('/api/v1/metrics/')
    assert resp.status_code == HTTPStatus.OK
    assert 'next_url' in resp.json
    assert 'prev_url' not in resp.json


def test_docs_are_valid():
    assert dict(error="Unable to render schema") != SERVER.API_V1.__schema__
