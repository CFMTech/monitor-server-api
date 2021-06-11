# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from http import HTTPStatus


def test_contexts_get(monitor, gen):
    monitor.assert_no_contexts()
    c = gen.new_context()
    monitor.post_contexts_v1(c)
    resp = monitor.client.get(f'/api/v1/contexts/{c["h"][:4]}')
    assert 'contexts' in resp.json
    assert resp.json['contexts']
    assert resp.json['contexts'][0] == c


def test_contexts_get_all(monitor, gen):
    for _ in range(4):
        c = gen.new_context()
        monitor.post_contexts_v1(c)
    monitor.assert_context_count(4)
    resp = monitor.client.get(f'/api/v1/contexts/')
    assert resp.status_code == HTTPStatus.OK


def test_contexts_count(monitor, gen):
    monitor.assert_no_contexts()
    for _ in range(4):
        c = gen.new_context()
        monitor.post_contexts_v1(c)
    monitor.assert_context_count(4)


def test_list_contexts_metrics(monitor, gen):
    s = gen.new_session()
    c1, c2 = gen.new_context(), gen.new_context()
    monitor.post_contexts_v1(c1, c2)
    for i in range(5):
        m = gen.new_metric(c1, s, item=f'item_c1_{i}')
        monitor.post_metrics_v1(m)
    for i in range(3):
        m = gen.new_metric(c2, s, item=f'item_c2_{i}')
        monitor.post_metrics_v1(m)

    resp = monitor.client.get(f'/api/v1/contexts/{c1["h"] + c2["h"]}/metrics')
    assert resp.status_code == HTTPStatus.NO_CONTENT
    resp = monitor.client.get(f'/api/v1/contexts/{c1["h"]}/metrics')
    assert resp.status_code == HTTPStatus.OK

    for i in resp.json['metrics']:
        assert i['context_h'] == c1['h']
        assert i['item'].startswith('item_c1_')
    assert len(resp.json['metrics']) == 5


def test_count_contexts_metrics(monitor, gen):
    s = gen.new_session()
    c1, c2 = gen.new_context(), gen.new_context()
    monitor.post_contexts_v1(c1, c2)
    for i in range(5):
        m = gen.new_metric(c1, s, item=f'item_c1_{i}')
        monitor.post_metrics_v1(m)
    for i in range(3):
        m = gen.new_metric(c2, s, item=f'item_c2_{i}')
        monitor.post_metrics_v1(m)

    resp = monitor.client.get(f'/api/v1/contexts/{c1["h"] + c2["h"]}/metrics/count')
    assert resp.status_code == HTTPStatus.OK
    assert 0 == resp.json['count']
    resp = monitor.client.get(f'/api/v1/contexts/{c1["h"]}/metrics/count')
    assert resp.status_code == HTTPStatus.OK
    assert 5 == resp.json['count']
