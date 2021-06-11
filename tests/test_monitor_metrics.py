# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from http import HTTPStatus
import pytest


def test_metrics_get(monitor, gen):
    c, s = gen.new_context(), gen.new_session()
    m = gen.new_metric(c, s)
    monitor.post_metrics_v1(m)
    resp = monitor.client.get('/api/v1/metrics/')
    assert 'metrics' in resp.json
    assert resp.json['metrics']
    assert resp.json['metrics'][0] == m


def test_metrics_post(monitor, gen):
    c, s = gen.new_context(), gen.new_session()
    m = gen.new_metric(c, s)
    resp = monitor.client.post('/api/v1/metrics/', json=m)
    assert resp.status_code == HTTPStatus.CREATED
    assert resp.json == m
    monitor.assert_metric_count(1)


@pytest.mark.parametrize('key', ['session_h', 'context_h', 'item_start_time', 'item_path',
                                 'item', 'item_variant', 'item_fs_loc', 'kind', 'component',
                                 'total_time', 'user_time', 'kernel_time', 'cpu_usage',
                                 'mem_usage'])
def test_metrics_post_missing_fields(client, gen, key):
    c, s = gen.new_context(), gen.new_session()
    m = gen.new_metric(c, s)
    del m[key]
    resp = client.post('/api/v1/metrics/', json=m)
    assert resp.status_code == HTTPStatus.BAD_REQUEST


def test_metrics_by_item(monitor, gen):
    # Lets generate 200 metrics
    c, s = gen.new_context(), gen.new_session()
    for _ in range(200):
        m = gen.new_metric(c, s, item='this_item')
        monitor.post_metrics_v1(m)
    resp = monitor.client.get('/api/v1/items/this_item/metrics')
    assert 'metrics' in resp.json
    assert resp.json['metrics']
    assert resp.json['metrics'][0]['item'] == 'this_item'
    assert 'next_url' in resp.json
    assert 'prev_url' not in resp.json


def test_count_metrics_by_item(monitor, gen):
    # Lets generate 200 metrics
    c, s = gen.new_context(), gen.new_session()
    for _ in range(200):
        m = gen.new_metric(c, s, item='this_item')
        monitor.post_metrics_v1(m)
    resp = monitor.client.get('/api/v1/items/this_item/metrics/count')
    assert resp.json == dict(count=200)


def test_metrics_by_session(monitor, gen):
    # Lets generate 200 metrics
    c, s1, s2 = gen.new_context(), gen.new_session(), gen.new_session()
    for _ in range(100):
        m = gen.new_metric(c, s1, item='this_item')
        monitor.post_metrics_v1(m)
    for _ in range(100):
        m = gen.new_metric(c, s2, item='that_item')
        monitor.post_metrics_v1(m)

    resp = monitor.client.get(f'/api/v1/sessions/{s1["session_h"]}/metrics')
    assert 'total_page' in resp.json
    assert resp.json['total_page'] == 20
    for page in range(1, resp.json['total_page']):
        assert resp.status_code == HTTPStatus.OK
        assert 'metrics' in resp.json
        assert resp.json['metrics']
        for metric in resp.json['metrics']:
            assert metric['item'] == 'this_item'
        resp = monitor.client.get(resp.json['next_url'])
    assert 'next_url' not in resp.json


def test_metrics_by_session_with_bad_session(monitor, gen):
    # Lets generate 200 metrics
    c, s1, s2 = gen.new_context(), gen.new_session(), gen.new_session()
    for _ in range(100):
        m = gen.new_metric(c, s1, item='this_item')
        monitor.post_metrics_v1(m)

    resp = monitor.client.get(f'/api/v1/sessions/{s2["session_h"]}/metrics')
    assert resp.status_code == HTTPStatus.NO_CONTENT


def test_metrics_by_contexts(monitor, gen):
    # Lets generate 200 metrics
    c1, c2, s = gen.new_context(), gen.new_context(), gen.new_session()
    for _ in range(100):
        m = gen.new_metric(c1, s, item='this_item')
        monitor.post_metrics_v1(m)
    for _ in range(100):
        m = gen.new_metric(c2, s, item='that_item')
        monitor.post_metrics_v1(m)

    resp = monitor.client.get(f'/api/v1/contexts/{c1["h"]}/metrics')
    assert 'total_page' in resp.json
    assert resp.json['total_page'] == 20
    for page in range(1, resp.json['total_page']):
        assert resp.status_code == HTTPStatus.OK
        assert 'metrics' in resp.json
        assert resp.json['metrics']
        for metric in resp.json['metrics']:
            assert metric['item'] == 'this_item'
        resp = monitor.client.get(resp.json['next_url'])
    assert 'next_url' not in resp.json


def test_metrics_by_session_with_bad_context(monitor, gen):
    # Lets generate 200 metrics
    c1, c2, s = gen.new_context(), gen.new_context(), gen.new_session()
    for _ in range(100):
        m = gen.new_metric(c1, s, item='this_item')
        monitor.post_metrics_v1(m)

    resp = monitor.client.get(f'/api/v1/contexts/{c2["h"]}/metrics')
    assert resp.status_code == HTTPStatus.NO_CONTENT


def test_count_metrics(monitor, gen):
    # Lets generate 80 metrics
    c, s1, s2 = gen.new_context(), gen.new_session(scm_ref='ABCDEF'), gen.new_session(scm_ref='ABCGHI')
    monitor.post_sessions_v1(s1, s2)
    for _ in range(40):
        m = gen.new_metric(c, s1, item='this_item')
        monitor.post_metrics_v1(m)
    for _ in range(40):
        m = gen.new_metric(c, s2, item='that_item')
        monitor.post_metrics_v1(m)
    monitor.assert_metric_count(80)
    assert 80 == monitor.client.get('/api/v1/filters/scm/ABC/metrics/count').json['count']
    assert 40 == monitor.client.get(f'/api/v1/filters/scm/{s1["scm_ref"]}/metrics/count').json['count']
    assert 0 == monitor.client.get('/api/v1/filters/scm/XYZ/metrics/count').json['count']


def test_count_metrics_by_session(monitor, gen):
    # Lets generate 200 metrics
    c, s1, s2 = gen.new_context(), gen.new_session(), gen.new_session()
    for _ in range(100):
        m = gen.new_metric(c, s1, item='this_item')
        monitor.post_metrics_v1(m)
    for _ in range(100):
        m = gen.new_metric(c, s2, item='that_item')
        monitor.post_metrics_v1(m)

    resp = monitor.client.get(f'/api/v1/sessions/{s1["session_h"]}/metrics/count')
    assert 'count' in resp.json
    assert resp.json['count'] == 100


def test_count_metrics_by_session_with_bad_session(monitor, gen):
    # Lets generate 200 metrics
    c1, c2, s = gen.new_context(), gen.new_context(), gen.new_session()
    for _ in range(100):
        m = gen.new_metric(c1, s, item='this_item')
        monitor.post_metrics_v1(m)
    for _ in range(100):
        m = gen.new_metric(c2, s, item='that_item')
        monitor.post_metrics_v1(m)

    resp = monitor.client.get(f'/api/v1/contexts/{c1["h"]}/metrics/count')
    assert 'count' in resp.json
    assert resp.json['count'] == 100


def test_metrics_by_scm_id(monitor, gen):
    # Lets generate 200 metrics
    c, s1, s2 = gen.new_context(), gen.new_session(), gen.new_session()
    monitor.post_sessions_v1(s1, s2)
    for _ in range(100):
        m = gen.new_metric(c, s1, item='this_item')
        monitor.post_metrics_v1(m)
    for _ in range(100):
        m = gen.new_metric(c, s2, item='that_item')
        monitor.post_metrics_v1(m)

    resp = monitor.client.get(f'/api/v1/filters/scm/{s1["scm_ref"] + "bad"}/metrics')
    assert resp.status_code == HTTPStatus.NO_CONTENT

    resp = monitor.client.get(f'/api/v1/filters/scm/{s1["scm_ref"]}/metrics')
    assert resp.status_code == HTTPStatus.OK
    assert 'total_page' in resp.json
    assert resp.json['total_page'] == 20
    for page in range(1, resp.json['total_page']):
        assert resp.status_code == HTTPStatus.OK
        assert 'metrics' in resp.json
        assert resp.json['metrics']
        for metric in resp.json['metrics']:
            assert metric['session_h'] == s1['session_h']
            assert metric['item'] == 'this_item'
        resp = monitor.client.get(resp.json['next_url'])
    assert 'next_url' not in resp.json


def test_metrics_by_variant(monitor, gen):
    c, s = gen.new_context(), gen.new_session()
    monitor.post_sessions_v1(s)
    assert monitor.client.get('/api/v1/metrics/count').json == dict(count=0)
    for i in range(10):
        variant = f'item_variant{i}'
        for _ in range(10):
            m = gen.new_metric(c, s, item_variant=variant, item=f'item{i}')
            monitor.post_metrics_v1(m)
    assert monitor.client.get('/api/v1/variants/item_variant5/metrics').status_code == HTTPStatus.OK
    r = monitor.client.get('/api/v1/variants/like/variant5/metrics')
    assert r.status_code == HTTPStatus.OK
    assert len(r.json['metrics']) == 5


def test_count_metrics_by_variant(monitor, gen):
    c, s = gen.new_context(), gen.new_session()
    monitor.post_sessions_v1(s)
    assert monitor.client.get('/api/v1/metrics/count').json == dict(count=0)
    for i in range(10):
        variant = f'item_variant{i}'
        for _ in range(i):
            m = gen.new_metric(c, s, item_variant=variant, item=f'item{i}')
            monitor.post_metrics_v1(m)
    resp = monitor.client.get('/api/v1/variants/item_variant5/metrics/count')
    assert resp.json == dict(count=5)


@pytest.mark.parametrize(['scope', 'count'], [('function', 5), ('module', 4), ('package', 3)])
def test_metrics_by_scope(monitor, gen, scope, count):
    c, s = gen.new_context(), gen.new_session()
    r = monitor.client.get(f'/api/v1/filters/scope/{scope}/metrics', json=s)
    assert r.status_code == HTTPStatus.NO_CONTENT
    for i in range(count):
        m = gen.new_metric(c, s, kind=scope, item=f'{scope}{i}')
        monitor.post_metrics_v1(m)

    resp = monitor.client.get(f'/api/v1/filters/scope/{scope}/metrics')
    assert resp.status_code == HTTPStatus.OK
    assert count == len(resp.json['metrics'])
    for i in range(count):
        assert resp.json['metrics'][i]['kind'] == scope


def test_count_metrics_by_scope(monitor, gen):
    c, s = gen.new_context(), gen.new_session()
    for scope in ['function', 'module', 'package']:
        url = f'/api/v1/filters/scope/{scope}/metrics'
        assert monitor.client.get(url, json=s).status_code == HTTPStatus.NO_CONTENT
    for i in range(3):
        m = gen.new_metric(c, s, kind='module', item=f'module{i}')
        monitor.post_metrics_v1(m)

    resp = monitor.client.get(f'/api/v1/filters/scope/module/metrics/count')
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == dict(count=3)

    for i in range(4):
        m = gen.new_metric(c, s, kind='package', item=f'package{i}')
        monitor.post_metrics_v1(m)
    resp = monitor.client.get(f'/api/v1/filters/scope/module/metrics/count')
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == dict(count=3)
    resp = monitor.client.get(f'/api/v1/filters/scope/package/metrics/count')
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == dict(count=4)

    for i in range(5):
        m = gen.new_metric(c, s, item=f'function{i}')
        monitor.post_metrics_v1(m)
    resp = monitor.client.get(f'/api/v1/filters/scope/module/metrics/count')
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == dict(count=3)
    resp = monitor.client.get(f'/api/v1/filters/scope/package/metrics/count')
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == dict(count=4)
    resp = monitor.client.get(f'/api/v1/filters/scope/function/metrics/count')
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == dict(count=5)


def test_metrics_by_item_pattern(monitor, gen):
    c, s = gen.new_context(), gen.new_session()
    monitor.post_sessions_v1(s)
    for _ in range(5):
        m = gen.new_metric(c, s, item='this_item')
        monitor.post_metrics_v1(m)
    for _ in range(5):
        m = gen.new_metric(c, s, item='that_item')
        monitor.post_metrics_v1(m)
    for _ in range(5):
        m = gen.new_metric(c, s, item='an_item')
        monitor.post_metrics_v1(m)

    assert monitor.client.get('/api/v1/items/like/nothing/metrics').status_code == HTTPStatus.NO_CONTENT
    resp = monitor.client.get('/api/v1/items/like/this/metrics')
    assert resp.status_code == HTTPStatus.OK
    assert 5 == len(resp.json['metrics'])
    for i in range(5):
        assert 'this_item' == resp.json['metrics'][i]['item']

    resp = monitor.client.get('/api/v1/items/like/item/metrics')
    assert resp.status_code == HTTPStatus.OK
    assert 3 == resp.json['total_page']
