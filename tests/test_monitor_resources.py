# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT


def test_list_head_resources_on_all_metrics(monitor, gen):
    # Lets generate 200 metrics
    c, s = gen.new_context(), gen.new_session()
    for i in range(200):
        mem = abs(100 - i) * 100
        m = gen.new_metric(c, s, item='this_item', mem_usage=mem)
        monitor.post_metrics_v1(m)
    resp = monitor.client.get('/api/v1/resources/memory/head/15/metrics')
    jdata = resp.json
    assert 'metrics' in jdata
    assert jdata['metrics']
    # Extract memory_usage and challenge against expected
    memory_use = sorted([int(metric['mem_usage']) for metric in jdata['metrics']], reverse=True)
    assert memory_use == [10000, 9900, 9900, 9800, 9800,
                          9700, 9700, 9600, 9600, 9500,
                          9500, 9400, 9400, 9300, 9300]


def test_list_tail_memory_on_all_metrics(monitor, gen):
    # Lets generate 200 metrics
    c, s = gen.new_context(), gen.new_session()
    for i in range(200):
        mem = abs(100 - i) * 100
        m = gen.new_metric(c, s, item='this_item', mem_usage=mem)
        monitor.post_metrics_v1(m)
    resp = monitor.client.get('/api/v1/resources/memory/tail/15/metrics')
    jdata = resp.json
    assert 'metrics' in jdata
    assert jdata['metrics']
    # Extract memory_usage and challenge against expected
    memory_use = sorted([int(metric['mem_usage']) for metric in jdata['metrics']], reverse=True)
    assert memory_use == [700, 700, 600, 600, 500,
                          500, 400, 400, 300, 300,
                          200, 200, 100, 100, 0]


def test_list_head_memory_on_components(monitor, gen):
    # Lets generate 200 metrics
    c, s = gen.new_context(), gen.new_session()
    for i in range(100):
        mem = i * 100
        m = gen.new_metric(c, s, component="compA", item='this_item', mem_usage=mem)
        monitor.post_metrics_v1(m)
    for i in range(100):
        mem = i
        m = gen.new_metric(c, s, component="compB", item='this_item', mem_usage=mem)
        monitor.post_metrics_v1(m)
    resp = monitor.client.get('/api/v1/resources/memory/components/compB/head/5/metrics')
    jdata = resp.json
    assert 'metrics' in jdata
    assert jdata['metrics']
    # Extract memory_usage and challenge against expected
    memory_use = sorted([int(metric['mem_usage']) for metric in jdata['metrics']], reverse=True)
    assert memory_use == [99, 98, 97, 96, 95]
    for m in jdata["metrics"]:
        assert m['component'] == 'compB'


def test_list_tail_memory_on_components(monitor, gen):
    # Lets generate 200 metrics
    c, s = gen.new_context(), gen.new_session()
    for i in range(100):
        mem = (i + 10) * 100
        m = gen.new_metric(c, s, component="compA", item='this_item', mem_usage=mem)
        monitor.post_metrics_v1(m)
    for i in range(100):
        mem = i
        m = gen.new_metric(c, s, component="compB", item='this_item', mem_usage=mem)
        monitor.post_metrics_v1(m)
    resp = monitor.client.get('/api/v1/resources/memory/components/compB/tail/5/metrics')
    jdata = resp.json
    assert 'metrics' in jdata
    assert jdata['metrics']
    # Extract memory_usage and challenge against expected
    memory_use = sorted([int(metric['mem_usage']) for metric in jdata['metrics']], reverse=True)
    assert memory_use == [4, 3, 2, 1, 0]
    for m in jdata["metrics"]:
        assert m['component'] == 'compB'


def test_list_head_memory_on_pipeline(monitor, gen):
    # Lets generate 200 metrics
    c = gen.new_context()
    s1, s2 = gen.new_session(pipeline_branch="pipeline1"), gen.new_session(pipeline_branch="pipeline2")
    monitor.post_sessions_v1(s1, s2)
    for i in range(100):
        mem = (i + 101) * 100
        m = gen.new_metric(c, s1, mem_usage=mem)
        monitor.post_metrics_v1(m)
    for i in range(100):
        mem = i
        m = gen.new_metric(c, s2, mem_usage=mem)
        monitor.post_metrics_v1(m)
    resp = monitor.client.get('/api/v1/resources/memory/pipelines/pipeline2/head/5/metrics')
    jdata = resp.json
    assert 'metrics' in jdata
    assert jdata['metrics']
    # Extract memory_usage and challenge against expected
    memory_use = sorted([int(metric['mem_usage']) for metric in jdata['metrics']], reverse=True)
    assert memory_use == [99, 98, 97, 96, 95]
    for m in jdata["metrics"]:
        assert m["session_h"] == s2["session_h"]


def test_list_tail_memory_on_pipeline(monitor, gen):
    # Lets generate 200 metrics
    c = gen.new_context()
    s1, s2 = gen.new_session(pipeline_branch="pipeline1"), gen.new_session(pipeline_branch="pipeline2")
    monitor.post_sessions_v1(s1, s2)
    for i in range(100):
        mem = (i + 101) * 100
        m = gen.new_metric(c, s1, mem_usage=mem)
        monitor.post_metrics_v1(m)
    for i in range(100):
        mem = i
        m = gen.new_metric(c, s2, mem_usage=mem)
        monitor.post_metrics_v1(m)
    resp = monitor.client.get('/api/v1/resources/memory/pipelines/pipeline2/tail/5/metrics')
    jdata = resp.json
    assert 'metrics' in jdata
    assert jdata['metrics']
    # Extract memory_usage and challenge against expected
    memory_use = sorted([int(metric['mem_usage']) for metric in jdata['metrics']], reverse=True)
    assert memory_use == [4, 3, 2, 1, 0]
    for m in jdata["metrics"]:
        assert m["session_h"] == s2["session_h"]


def test_list_head_memory_of_build(monitor, gen):
    # Lets generate 200 metrics
    c = gen.new_context()
    s1 = gen.new_session(pipeline_branch="pipeline1", pipeline_build_no="1")
    s2 = gen.new_session(pipeline_branch="pipeline1", pipeline_build_no="2")
    monitor.post_sessions_v1(s1, s2)
    for i in range(100):
        mem = (i + 101) * 100
        m = gen.new_metric(c, s1, mem_usage=mem)
        monitor.post_metrics_v1(m)
    for i in range(100):
        mem = i
        m = gen.new_metric(c, s2, mem_usage=mem)
        monitor.post_metrics_v1(m)
    resp = monitor.client.get('/api/v1/resources/memory/pipelines/pipeline1/builds/2/head/5/metrics')
    jdata = resp.json
    assert 'metrics' in jdata
    assert jdata['metrics']
    # Extract memory_usage and challenge against expected
    memory_use = sorted([int(metric['mem_usage']) for metric in jdata['metrics']], reverse=True)
    assert memory_use == [99, 98, 97, 96, 95]
    for m in jdata["metrics"]:
        assert m["session_h"] == s2["session_h"]


def test_list_tail_memory_of_build(monitor, gen):
    # Lets generate 200 metrics
    c = gen.new_context()
    s1 = gen.new_session(pipeline_branch="pipeline1", pipeline_build_no="1")
    s2 = gen.new_session(pipeline_branch="pipeline1", pipeline_build_no="2")
    monitor.post_sessions_v1(s1, s2)
    for i in range(100):
        mem = (i + 101) * 100
        m = gen.new_metric(c, s1, mem_usage=mem)
        monitor.post_metrics_v1(m)
    for i in range(100):
        mem = i
        m = gen.new_metric(c, s2, mem_usage=mem)
        monitor.post_metrics_v1(m)
    resp = monitor.client.get('/api/v1/resources/memory/pipelines/pipeline1/builds/2/tail/5/metrics')
    jdata = resp.json
    assert 'metrics' in jdata
    assert jdata['metrics']
    # Extract memory_usage and challenge against expected
    memory_use = sorted([int(metric['mem_usage']) for metric in jdata['metrics']], reverse=True)
    assert memory_use == [4, 3, 2, 1, 0]
    for m in jdata["metrics"]:
        assert m["session_h"] == s2["session_h"]
