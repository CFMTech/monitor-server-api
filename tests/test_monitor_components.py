# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from http import HTTPStatus


def test_components_get(monitor, gen):
    monitor.assert_no_components()
    c, s = gen.new_context(), gen.new_session()
    for i in "ABC":
        m = gen.new_metric(c, s, component=f'component_{i}')
        monitor.post_metrics_v1(m)
    resp = monitor.client.get(f'/api/v1/components/')
    assert 'components' in resp.json
    assert resp.json['components'] == ['component_A', 'component_B', 'component_C']


def test_component_get_with_pattern(monitor, gen):
    c, s = gen.new_context(), gen.new_session()
    for i in "ABC":
        m = gen.new_metric(c, s, component=f'component_{i}', item=f'item_{i}')
        monitor.post_metrics_v1(m)
    m = gen.new_metric(c, s, component=f'another_component', item='another_item')
    monitor.post_metrics_v1(m)
    m = gen.new_metric(c, s, component=f'another_component', item='another_item')
    monitor.post_metrics_v1(m)
    assert HTTPStatus.NO_CONTENT == monitor.client.get('/api/v1/components/BAD').status_code
    resp = monitor.client.get('/api/v1/components/component_')
    assert resp.json['components'] == ['component_A', 'component_B', 'component_C']


def test_count_components(monitor, gen):
    assert 0 == monitor.client.get(f'/api/v1/components/count').json['count']
    c, s = gen.new_context(), gen.new_session()
    for i in "ABC":
        m = gen.new_metric(c, s, component=f'component_{i}')
        monitor.post_metrics_v1(m)
    resp = monitor.client.get(f'/api/v1/components/count')
    assert resp.json['count'] == 3


def test_components_items_metrics(monitor, gen):
    url = f'/api/v1/components/comp_A/items/test_that/metrics'
    assert HTTPStatus.NO_CONTENT == monitor.client.get(url).status_code
    c, s = gen.new_context(), gen.new_session()
    for i in range(10):
        m = gen.new_metric(c, s, component=['comp_A', 'comp_B'][i % 2], item='test_that')
        monitor.post_metrics_v1(m)
    metrics = monitor.client.get(url).json["metrics"]
    assert 5 == len(metrics)


def test_components_items_metrics_no_component_assigned(monitor, gen):
    url = f'/api/v1/components/items/test_that/metrics'
    assert HTTPStatus.NO_CONTENT == monitor.client.get(url).status_code
    c, s = gen.new_context(), gen.new_session()
    for i in range(10):
        m = gen.new_metric(c, s, component='', item='test_that')
        monitor.post_metrics_v1(m)
    metrics = monitor.client.get(url)
    assert 5 == len(metrics.json['metrics'])
    assert 2 == metrics.json["total_page"]
    metrics = monitor.client.get(f'{url}?page=2')
    assert 5 == len(metrics.json["metrics"])


def test_components_variants_metrics(monitor, gen):
    url = f'/api/v1/components/comp_A/variants/test_that[1/metrics'
    assert HTTPStatus.NO_CONTENT == monitor.client.get(url).status_code
    c, s = gen.new_context(), gen.new_session()
    for i in range(10):
        m = gen.new_metric(c, s, component=['comp_A', 'comp_B'][i % 2], item_variant='test_that[1')
        monitor.post_metrics_v1(m)
    metrics = monitor.client.get(url).json["metrics"]
    assert 5 == len(metrics)


def test_components_variants_metrics_no_component_assigned(monitor, gen):
    url = f'/api/v1/components/variants/test_that[1/metrics'
    assert HTTPStatus.NO_CONTENT == monitor.client.get(url).status_code
    c, s = gen.new_context(), gen.new_session()
    for i in range(10):
        m = gen.new_metric(c, s, component='', item_variant='test_that[1')
        monitor.post_metrics_v1(m)
    metrics = monitor.client.get(url)
    assert 5 == len(metrics.json['metrics'])
    assert 2 == metrics.json["total_page"]
    metrics = monitor.client.get(f'{url}?page=2')
    assert 5 == len(metrics.json["metrics"])


def test_metrics_by_components(monitor, gen):
    c, s = gen.new_context(), gen.new_session()
    for i in range(3):
        m = gen.new_metric(c, s, component='', item=f'item_{i}')
        monitor.post_metrics_v1(m)
    for i in range(4):
        m = gen.new_metric(c, s, component=f'another_component', item='another_item')
        monitor.post_metrics_v1(m)

    assert HTTPStatus.NO_CONTENT == monitor.client.get('/api/v1/components/BAD/metrics').status_code
    resp = monitor.client.get('/api/v1/components/another_component/metrics')
    for m in resp.json['metrics']:
        assert m['item'] == 'another_item'
        assert m['component'] == 'another_component'
    assert 4 == len(resp.json['metrics'])
    resp = monitor.client.get('/api/v1/components/metrics')
    assert 3 == len(resp.json['metrics'])
    for m in resp.json['metrics']:
        assert m['item'] in ['item_1', 'item_2', 'item_0']
        assert not m['component']


def test_component_pipelines(monitor, gen):
    jsessions = gen.new_jenkins_session(buildno="1234")
    csessions = gen.new_circleci_session(buildno="9857677")
    ctx = gen.new_context()
    metric_comp_a = gen.new_metric(ctx, jsessions, component='compA')
    metric_comp_a_circle = gen.new_metric(ctx, csessions, component='compA')
    metric_comp_b = gen.new_metric(ctx, jsessions, component='compB')

    monitor.post_sessions_v1(jsessions, csessions)
    monitor.post_contexts_v1(ctx)
    monitor.post_metrics_v1(metric_comp_a, metric_comp_a_circle, metric_comp_b)

    pipelines = monitor.client.get('/api/v1/components/compA/pipelines')
    assert pipelines.status_code == HTTPStatus.OK
    assert pipelines.json == dict(component='compA',
                                  next_url=None, prev_url=None,
                                  pipelines=['jenkinsci:monitor', 'circleci:monitor'],
                                  total_page=1)


def test_component_sessions(monitor, gen):
    monitor.assert_no_sessions()
    c = gen.new_context()
    monitor.post_contexts_v1(c)
    for bno in range(1, 11):
        build_number = str(bno + 987654321)
        s1 = gen.new_circleci_session(buildno=build_number)
        s2 = gen.new_jenkins_session(buildno=build_number)
        monitor.post_sessions_v1(s1, s2)
        monitor.post_metrics_v1(gen.new_metric(c, s1, component="compA"))
        monitor.post_metrics_v1(gen.new_metric(c, s2, component="compA"))
        if bno % 2 == 0:
            s3 = gen.new_circleci_session(buildno=build_number)
            monitor.post_sessions_v1(s3)
            monitor.post_metrics_v1(gen.new_metric(c, s3, component="compA"))
    monitor.assert_session_count(25)

    resp = monitor.client.get('/api/v1/components/compA/pipelines/circleci:monitor/builds')
    assert resp.status_code == HTTPStatus.OK
