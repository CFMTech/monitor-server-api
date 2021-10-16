# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from monitor_api.enums import Field, MetricScope
from monitor_api.core.collections import Contexts, Metrics, Sessions
from monitor_api.core.entities import Context, Metric, Session
from monitor_api.py36 import fromisoformat
import numpy as np
import pandas as pd


def test_collection_sessions_basic(gen):
    s = Sessions()
    h = [gen.random_string() for _ in range(10)]
    scm = [gen.random_string() for _ in range(10)]
    start_date = [f'2020-04-26T{i}:00:52.372833' for i in range(11, 21)]
    tags = [dict(python="3.6.8", build_branch="pipeline", build_no=i) for i in range(10, 16)]
    tags.extend([dict(python="3.8.2", project="test", build_branch="pipeline-test", build_no=i) for i in range(1, 6)])
    assert len(s) == 0
    for _h, _s, _d, _t in zip(h, scm, start_date, tags):
        s[_h] = Session(_h, _s, _d, _t)
    assert len(s) == 10

    filtered_sessions = s.with_tags('python')
    assert len(filtered_sessions) == 10
    assert len(s.with_tags(python="3.6.8")) == 6
    assert not s.with_tags(python="3.6.8", weird_tag='none match')
    session = s.with_tags('python', build_no=13)
    assert len(session) == 1
    assert h[3] in session
    real_session = session[h[3]]
    assert real_session.h == h[3]
    assert real_session.scm == scm[3]
    assert real_session.start_date.hour == 14
    assert real_session.tags == dict(python="3.6.8", build_branch="pipeline", build_no=13)
    assert not len(s.with_tags('python3', build_no=13))


def test_collection_session_with_scm(gen):
    s = Sessions()
    h = [gen.random_string() for _ in range(10)]
    scm = [f'scm_ref{i}' for i in range(5)] * 2
    start_date = [f'2020-04-26T{i}:00:52.372833' for i in range(11, 21)]
    tags = [dict(python="3.6.8", build_branch="pipeline", build_no=i) for i in range(10, 16)]
    tags.extend([dict(python="3.8.2", project="test", build_branch="pipeline-test", build_no=i) for i in range(1, 6)])
    for _h, _s, _d, _t in zip(h, scm, start_date, tags):
        s[_h] = Session(_h, _s, _d, _t)

    session_scm_ref_4 = s.with_scm('scm_ref_4')
    assert not len(session_scm_ref_4)
    session_scm_ref_4 = s.with_scm('scm_ref4')
    assert len(session_scm_ref_4) == 2


def test_collection_session_cm(gen):
    s = Sessions()
    h = [gen.random_string() for _ in range(10)]
    scm = [f'scm_ref{i}' for i in range(5)] * 2
    start_date = [f'2020-04-26T{i}:00:52.372833' for i in range(11, 21)]
    tags = [dict(python="3.6.8", build_branch="pipeline", build_no=i) for i in range(10, 16)]
    tags.extend([dict(python="3.8.2", project="test", build_branch="pipeline-test", build_no=i) for i in range(1, 6)])
    for _h, _s, _d, _t in zip(h, scm, start_date, tags):
        s[_h] = Session(_h, _s, _d, _t)

    with s.with_scm('scm_ref4') as filtered_sessions:
        assert len(filtered_sessions) == 2


def test_collection_sessions_export_pandas(gen):
    s = Sessions()
    h = ['anyhashvalue1', 'anyhashvalue2', 'anyhashvalue3']
    scm = ['anysha1value1', 'anysha1value2', 'anysha1value3']
    start_date = [f'2020-04-26T{i}:00:52.372833' for i in range(10, 13)]
    tags = [dict(python="3.6.8", build_branch="pipeline", build_no=i) for i in range(10, 13)]
    df_ref = pd.DataFrame(columns=['session_h', 'run_date', 'scm', 'python', 'build_branch', 'build_no'])
    loc = 0
    for _h, _s, _d, _t in zip(h, scm, start_date, tags):
        if _h == 'anyhashvalue2':
            s[_h] = Session(_h, _s, _d)
            df_ref.loc[loc] = [_h, fromisoformat(_d), _s, np.NaN, np.NaN, np.NaN]
        else:
            s[_h] = Session(_h, _s, _d, _t)
            df_ref.loc[loc] = [_h, fromisoformat(_d), _s,
                               _t['python'], _t['build_branch'], float(_t['build_no'])]
        loc += 1
    df = s.to_df()
    assert df.shape == (3, 6)
    assert df.equals(df_ref)
    df = s.to_df(keep=[Field.SESSION_H, Field.SCM])
    assert df.shape == (3, 2)
    df_expected = df_ref.copy()
    df_expected.drop(columns=['run_date', 'python', 'build_branch', 'build_no'], inplace=True)
    assert df.equals(df_expected)
    df = s.to_df(keep=[Field.SESSION_H, Field.SCM], drop=[Field.TAGS])
    assert df.shape == (3, 2)
    assert df.equals(df_expected)
    df = s.to_df(drop=[Field.SESSION_H, Field.TAGS])
    assert df.shape == (3, 2)
    df_expected = df_ref.copy()
    df_expected.drop(columns=['session_h', 'python', 'build_no', 'build_branch'], inplace=True)
    assert df.equals(df_expected)


def test_collection_sessions_export_yaml(gen):
    s = Sessions()
    h = ['anyhashvalue1', 'anyhashvalue2', 'anyhashvalue3']
    scm = ['anysha1value1', 'anysha1value2', 'anysha1value3']
    start_date = [f'2020-04-26T{i}:00:52.372833' for i in range(10, 13)]
    tags = [dict(python="3.6.8", build_branch="pipeline", build_no=i) for i in range(10, 13)]
    for _h, _s, _d, _t in zip(h, scm, start_date, tags):
        if _h == 'anyhashvalue2':
            s[_h] = Session(_h, _s, _d)
        else:
            s[_h] = Session(_h, _s, _d, _t)
    assert str(s) == '''sessions:
  anyhashvalue1:
    run_date: 2020-04-26 10:00:52.372833
    scm: anysha1value1
    tags:
      build_branch: pipeline
      build_no: 10
      python: 3.6.8
  anyhashvalue2:
    run_date: 2020-04-26 11:00:52.372833
    scm: anysha1value2
  anyhashvalue3:
    run_date: 2020-04-26 12:00:52.372833
    scm: anysha1value3
    tags:
      build_branch: pipeline
      build_no: 12
      python: 3.6.8
'''


def test_collection_sessions_filter(gen):
    s = Sessions()
    h = [gen.random_string() for _ in range(10)]
    scm = [gen.random_string() for _ in range(10)]
    start_date = [f'2020-04-26T{i}:00:52.372833' for i in range(11, 21)]
    tags = [dict(python="3.6.8", build_branch="pipeline", build_no=i) for i in range(10, 16)]
    tags.extend([dict(python="3.8.2", project="test", build_branch="pipeline-test", build_no=i) for i in range(1, 6)])
    for _h, _s, _d, _t in zip(h, scm, start_date, tags):
        s[_h] = Session(_h, _s, _d, _t)
    assert len(s) == 10

    def filter_session(sv: Session):
        return int(sv.tags['build_no']) % 2 == 0

    assert len(s.filter_with(filter_session)) == 5
    assert len(s.filter_with(filter_session, inplace=True)) == 5
    assert s.filter_with(filter_session) == s.filter_with(filter_session, inplace=True)


def test_collection_contexts_basic(gen):
    c = Contexts()
    h = [gen.random_string() for _ in range(10)]
    hosts = [gen.random_string() for _ in range(10)]
    for i, (_h, host) in enumerate(zip(h, hosts)):
        c[_h] = Context(_h, i + 1, (i + 1) * 100, 'i386' if i % 2 == 0 else 'i786', 'Intel' if i % 2 == 0 else "",
                        3000 * (i + 1), host, 'x86' if i % 2 == 0 else 'x86_64', '32bits' if i % 2 == 0 else '64bits',
                        host[::-1], host[::2])
    assert len(c) == 10
    assert h[5] in c
    real_context = c[h[5]]
    assert real_context.h == h[5]
    assert real_context.cpu_count == 6
    assert real_context.cpu_freq == 600
    assert not real_context.cpu_vendor
    assert real_context.cpu_type == 'i786'
    assert real_context.total_ram == 18000
    assert real_context.machine_node == hosts[5]
    assert real_context.machine_type == 'x86_64'
    assert real_context.machine_arch == '64bits'
    assert real_context.sys_info == hosts[5][::-1]
    assert real_context.python_info == hosts[5][::2]


def test_collection_contexts_export_pandas(gen):
    c = Contexts()
    exp_df = pd.DataFrame(columns=['context_h', 'cpu_count', 'cpu_freq', 'cpu_type', 'cpu_vendor',
                                   'arch', 'hostname', 'type', 'ram', 'sys', 'py'])
    h = [gen.random_string() for _ in range(10)]
    hosts = [gen.random_string() for _ in range(10)]
    for i, (_h, host) in enumerate(zip(h, hosts)):
        if i % 2 == 0:
            c[_h] = Context(_h, i + 1, (i + 1) * 100, 'i386', 'Intel', 3000 * (i + 1), host, 'x86', '32bits',
                            host[::-1], host[::2])
            exp_df.loc[i] = [_h, i + 1, (i + 1) * 100, 'i386', 'Intel', '32bits', host, 'x86', 3000 * (i + 1),
                             host[::-1], host[::2]]
        else:
            c[_h] = Context(_h, i + 1, (i + 1) * 100, 'i786', '', 3000 * (i + 1), host, 'x86_64', '64bits',
                            host[::-1], host[::2])
            exp_df.loc[i] = [_h, i + 1, (i + 1) * 100, 'i786', '', '64bits', host, 'x86_64', 3000 * (i + 1),
                             host[::-1], host[::2]]
    exp_df = exp_df.astype(dict(cpu_count='int64', cpu_freq='int64', ram='int64'))
    df = c.to_df()
    assert df.shape == (10, 11)
    assert df.equals(exp_df)


def test_collection_contexts_export_yaml(gen):
    h = ['anyhashvalue1', 'anyhashvalue2', 'anyhashvalue3']
    hosts = ['host1', 'host2', 'host3']
    c = Contexts()
    for i, (_h, host) in enumerate(zip(h, hosts)):
        c[_h] = Context(_h, i + 1, (i + 1) * 100, 'i386', 'Intel', 3000 * (i + 1), host, 'x86', '32bits',
                        host[::-1], host[::2])
    assert str(c) == '''contexts:
  anyhashvalue1:
    arch: 32bits
    cpu_count: 1
    cpu_freq: 100
    cpu_type: i386
    cpu_vendor: Intel
    hostname: host1
    py: hs1
    ram: 3000
    sys: 1tsoh
    type: x86
  anyhashvalue2:
    arch: 32bits
    cpu_count: 2
    cpu_freq: 200
    cpu_type: i386
    cpu_vendor: Intel
    hostname: host2
    py: hs2
    ram: 6000
    sys: 2tsoh
    type: x86
  anyhashvalue3:
    arch: 32bits
    cpu_count: 3
    cpu_freq: 300
    cpu_type: i386
    cpu_vendor: Intel
    hostname: host3
    py: hs3
    ram: 9000
    sys: 3tsoh
    type: x86
'''


def test_collection_contexts_filter(gen):
    c = Contexts()
    h = [gen.random_string() for _ in range(10)]
    hosts = [gen.random_string() for _ in range(10)]
    for i, (_h, host) in enumerate(zip(h, hosts)):
        if i % 2 == 0:
            c[_h] = Context(_h, i + 1, (i + 1) * 100, 'i386', 'Intel', 3000 * (i + 1), host, 'x86', '32bits',
                            host[::-1], host[::2])
        else:
            c[_h] = Context(_h, i + 1, (i + 1) * 100, 'i786', '', 3000 * (i + 1), host, 'x86_64', '64bits',
                            host[::-1], host[::2])

    def keep_ram_above_9k(ctx: Context):
        return ctx.total_ram > 9000

    c.filter_with(keep_ram_above_9k, inplace=True)
    assert len(c) == 7
    assert len(c.filter_with(keep_ram_above_9k)) == 7


def test_collection_contexts_cm(gen):
    c = Contexts()
    h = [gen.random_string() for _ in range(10)]
    hosts = [gen.random_string() for _ in range(10)]
    for i, (_h, host) in enumerate(zip(h, hosts)):
        if i % 2 == 0:
            c[_h] = Context(_h, i + 1, (i + 1) * 100, 'i386', 'Intel', 3000 * (i + 1), host, 'x86', '32bits',
                            host[::-1], host[::2])
        else:
            c[_h] = Context(_h, i + 1, (i + 1) * 100, 'i786', '', 3000 * (i + 1), host, 'x86_64', '64bits',
                            host[::-1], host[::2])

    def keep_ram_above_9k(ctx: Context):
        return ctx.total_ram > 9000

    with c.filter_with(keep_ram_above_9k) as contexts_with_9k_ram_or_above:
        assert len(contexts_with_9k_ram_or_above) == 7
        for context in contexts_with_9k_ram_or_above.values():
            assert context.total_ram >= 9000


def test_collection_metrics_basic(gen):
    m = Metrics()
    c = gen.random_strings(10)
    s = gen.random_strings(10)
    ipaths = gen.random_pypaths(10, 3)
    items = gen.random_strings(10)
    variants = gen.random_strings(10)
    paths = gen.random_paths(10, 5)
    components = gen.random_strings(10)
    walls = gen.random_floats(10, 1, 10)
    users = gen.random_floats(10, 1, 10)
    kernels = gen.random_floats(10, 1, 10)
    cpuse = gen.random_floats(10, 1, 10)
    mems = gen.random_floats(10, 1, 100)
    for i in range(10):
        m.append(Metric(context_h=c[i], session_h=s[i], start_time=f'2020-04-26T{10+i}:00:52.372833',
                        item_path=ipaths[i], item=items[i], variant=variants[i], path=paths[i],
                        kind=MetricScope.FUNCTION, component=components[i],
                        wall_time=walls[i], user_time=users[i], kernel_time=kernels[i],
                        cpu_usage=cpuse[i], memory_usage=mems[i]))
    assert len(m) == 10
    metric = m[3]
    assert metric.context == c[3]
    assert metric.session == s[3]
    assert metric.component == components[3]
    assert metric.run_time == fromisoformat('2020-04-26T13:00:52.372833')
    assert metric.item_path == ipaths[3]
    assert metric.item == items[3]
    assert metric.variant == variants[3]
    assert metric.scope == MetricScope.FUNCTION
    assert metric.path == paths[3]
    assert metric.wall_time == walls[3]
    assert metric.user_time == users[3]
    assert metric.kernel_time == kernels[3]
    assert metric.cpu_usage == cpuse[3]
    assert metric.memory_usage == mems[3]


def test_collection_metrics_export_pandas(gen):
    m = Metrics()
    ch = ['contexthashvalue1', 'contexthashvalue2', 'contexthashvalue3']
    sh = ['sessionsha1value1', 'sessionsha1value2', 'sessionsha1value3']
    df_exp = pd.DataFrame(columns=['context_h', 'session_h', 'start_time', 'item_path', 'item', 'path',
                                   'variant', 'kind', 'wall_time', 'user_time', 'kernel_time', 'cpu_usage',
                                   'memory_usage', 'component'])
    for i, (c, s) in enumerate(zip(ch, sh)):
        m.append(Metric(context_h=c, session_h=s, start_time=f'2020-04-26T{10 + i}:00:52.372833',
                        item_path=f'item.path._{i}', item=f'test_{i}', variant=f'test_{i}',
                        path=f'/path/to/test/{i}', kind=MetricScope.FUNCTION, component=f'comp_{i}',
                        wall_time=1 + i * 3.14, user_time=1 + i * 2.718, kernel_time=1 + i * 0.4, cpu_usage=100 + i,
                        memory_usage=314 * (i + 1)))
        df_exp.loc[i] = [c, s, fromisoformat(f'2020-04-26T{10 + i}:00:52.372833'),
                         f'item.path._{i}', f'test_{i}', f'/path/to/test/{i}', f'test_{i}', 'function',
                         1 + i * 3.14, 1 + i * 2.718, 1 + i * 0.4, 100 + i, 314 * (i + 1),
                         f'comp_{i}']

    df_exp = df_exp.astype(dict(user_time='float', kernel_time='float', wall_time='float',
                                cpu_usage='int64', memory_usage='int64'))
    df = m.to_df()
    assert df.equals(df_exp)


def test_collection_metrics_export_w_sessions_contexts_pandas():
    tags = dict(python="3.6.8", build_branch="pipeline", build_no='10')
    sessions = Sessions()
    contexts = Contexts()
    metrics = Metrics()
    session = sessions.add(Session('session_id', 'scmref', '2020-04-26T10:00:00', tags))
    ctx = contexts.add(Context('context_id', 4, 2500, 'i386', None, 16000, 'nodename',
                               'x86_64', '32bits', 'info', 'python'))
    df_exp = pd.DataFrame(columns=['session_h', 'context_h', 'item', 'cpu_count', 'ram',
                                   'scm', 'wall_time', 'memory_usage'])
    for i in range(5):
        metrics.append(Metric(context_h=ctx.h, session_h=session.h,
                              start_time=f'2020-04-26T{10 + i}:00:52.372833',
                              item_path=f'item.path._{i}', item=f'test_{i}', variant=f'test_{i}',
                              path=f'/path/to/test/{i}', kind=MetricScope.FUNCTION, component=f'comp_{i}',
                              wall_time=1 + i * 3.14, user_time=1 + i * 2.718, kernel_time=1 + i * 0.4,
                              cpu_usage=100 + i, memory_usage=314 * (i + 1)))
        df_exp.loc[i] = [session.h, ctx.h, f'test_{i}',
                         ctx.cpu_count, ctx.total_ram, session.scm, 1 + i * 3.14, 314 * (i + 1)]

    fields_to_keep = [Field.SESSION_H, Field.CONTEXT_H, Field.ITEM, Field.CPU_COUNT,
                      Field.RAM_TOTAL_MB, Field.SCM, Field.TOTAL_TIME, Field.MEM_USAGE]
    df = metrics.to_df(keep=fields_to_keep, sessions=sessions, contexts=contexts)
    df = df[[k.value for k in fields_to_keep]]
    df_exp = df_exp.astype(df.dtypes)
    assert df.equals(df_exp)


def test_collection_metrics_export_yaml(gen):
    m = Metrics()
    ch = ['contexthashvalue1', 'contexthashvalue2', 'contexthashvalue3']
    sh = ['sessionsha1value1', 'sessionsha1value2', 'sessionsha1value3']
    for i, (c, s) in enumerate(zip(ch, sh)):
        m.append(Metric(context_h=c, session_h=s, start_time=f'2020-04-26T{10+i}:00:52.372833',
                        item_path=f'item.path._{i}', item=f'test_{i}', variant=f'test_{i}',
                        path=f'/path/to/test/{i}', kind=MetricScope.FUNCTION, component=f'comp_{i}',
                        wall_time=1 + i * 3.14, user_time=1 + i * 2.718, kernel_time=1 + i * 0.4, cpu_usage=100 + i,
                        memory_usage=314 * (i + 1)))
    assert str(m) == '''metrics:
  metric_0:
    component: comp_0
    context_h: contexthashvalue1
    cpu_usage: 100
    item: test_0
    item_path: item.path._0
    kernel_time: 1.0
    kind: function
    memory_usage: 314
    path: /path/to/test/0
    session_h: sessionsha1value1
    start_time: 2020-04-26 10:00:52.372833
    user_time: 1.0
    variant: test_0
    wall_time: 1.0
  metric_1:
    component: comp_1
    context_h: contexthashvalue2
    cpu_usage: 101
    item: test_1
    item_path: item.path._1
    kernel_time: 1.4
    kind: function
    memory_usage: 628
    path: /path/to/test/1
    session_h: sessionsha1value2
    start_time: 2020-04-26 11:00:52.372833
    user_time: 3.718
    variant: test_1
    wall_time: 4.140000000000001
  metric_2:
    component: comp_2
    context_h: contexthashvalue3
    cpu_usage: 102
    item: test_2
    item_path: item.path._2
    kernel_time: 1.8
    kind: function
    memory_usage: 942
    path: /path/to/test/2
    session_h: sessionsha1value3
    start_time: 2020-04-26 12:00:52.372833
    user_time: 6.436
    variant: test_2
    wall_time: 7.28
'''


def test_collection_metrics_filter(gen):
    m = Metrics()
    c = gen.random_strings(10)
    s = gen.random_strings(10)
    ipaths = gen.random_pypaths(10, 3)
    items = gen.random_strings(10)
    variants = gen.random_strings(10)
    paths = gen.random_paths(10, 5)
    components = gen.random_strings(10)
    walls = gen.random_floats(10, 1, 10)
    users = gen.random_floats(10, 1, 10)
    kernels = gen.random_floats(10, 1, 10)
    cpuse = gen.random_floats(10, 1, 10)
    mems = gen.random_floats(10, 1, 100)
    for i in range(10):
        m.append(Metric(context_h=c[i], session_h=s[i], start_time=f'2020-04-26T{10 + i}:00:52.372833',
                        item_path=ipaths[i], item=items[i], variant=variants[i], path=paths[i],
                        kind=MetricScope.FUNCTION, component=components[i],
                        wall_time=walls[i], user_time=users[i], kernel_time=kernels[i],
                        cpu_usage=cpuse[i], memory_usage=mems[i]))
    assert len(m) == 10

    def keep_metric_after_17h(metric: Metric):
        return metric.run_time.hour > 17

    assert len(m.filter_with(keep_metric_after_17h)) == 2
    m.filter_with(keep_metric_after_17h, inplace=True)
    assert len(m) == 2


def test_merge_metrics(gen):
    m = Metrics()
    ch = ['contexthashvalue1', 'contexthashvalue2', 'contexthashvalue3']
    sh = ['sessionsha1value1', 'sessionsha1value2', 'sessionsha1value3']
    for i, (c, s) in enumerate(zip(ch, sh)):
        m.append(Metric(context_h=c, session_h=s, start_time=f'2020-04-26T{10 + i}:00:52.372833',
                        item_path=f'item.path._{i}', item=f'test_{i}', variant=f'test_{i}',
                        path=f'/path/to/test/{i}', kind=MetricScope.FUNCTION, component=f'comp_{i}',
                        wall_time=1 + i * 3.14, user_time=1 + i * 2.718, kernel_time=1 + i * 0.4, cpu_usage=100 + i,
                        memory_usage=314 * (i + 1)))

    m2 = Metrics.merge(m, m)
    assert m == m2

    m2 = Metrics()
    ch = ['contexthashvalue4', 'contexthashvalue5']
    sh = ['sessionsha1value4', 'sessionsha1value5']
    for i, (c, s) in enumerate(zip(ch, sh)):
        m.append(Metric(context_h=c, session_h=s, start_time=f'2020-04-26T{10 + i}:00:52.372833',
                        item_path=f'item.path._{i}', item=f'test_{i}', variant=f'test_{i}',
                        path=f'/path/to/test/{i}', kind=MetricScope.FUNCTION, component=f'comp_{i}',
                        wall_time=1 + i * 3.14, user_time=1 + i * 2.718, kernel_time=1 + i * 0.4, cpu_usage=100 + i,
                        memory_usage=314 * (i + 1)))

    m3 = Metrics.merge(m, m2)
    assert len(m3) == len(m) + len(m2)
    for metric in m:
        assert metric in m3
    for metric in m2:
        assert metric in m3


def test_collection_metric_cm(gen):
    m = Metrics()
    ch = ['contexthashvalue1', 'contexthashvalue2', 'contexthashvalue3']
    sh = ['sessionsha1value1', 'sessionsha1value2', 'sessionsha1value3']
    for i, (c, s) in enumerate(zip(ch, sh)):
        m.append(Metric(context_h=c, session_h=s, start_time=f'2020-04-26T{10 + i}:00:52.372833',
                        item_path=f'item.path._{i}', item=f'test_{i}', variant=f'test_{i}',
                        path=f'/path/to/test/{i}', kind=MetricScope.FUNCTION, component=f'comp_{i}',
                        wall_time=1 + i * 3.14, user_time=1 + i * 2.718, kernel_time=1 + i * 0.4, cpu_usage=100 + i,
                        memory_usage=314 * (i + 1)))

    with m.filter_with(lambda metric: metric.context == 'contexthashvalue1') as metric_first_contexts:
        assert len(metric_first_contexts) == 1
    with m.filter_with(lambda metric: metric.context == 'contexthashvalue10') as metric_invalid_contexts:
        assert not metric_invalid_contexts


def test_collection_metric_variants_of(gen):
    m = Metrics()
    ch = ['contexthashvalue1', 'contexthashvalue2', 'contexthashvalue3']
    sh = ['sessionsha1value1', 'sessionsha1value2', 'sessionsha1value3']
    for i, (c, s) in enumerate(zip(ch, sh)):
        test_name = 'test_that' if i % 2 == 0 else 'test_this'
        m.append(Metric(context_h=c, session_h=s, start_time=f'2020-04-26T{10 + i}:00:52.372833',
                        item_path=f'item.path._{i}', item=test_name, variant=f'{test_name}[{i}]',
                        path=f'/path/to/test/{i}', kind=MetricScope.FUNCTION, component=f'comp_{i}',
                        wall_time=1 + i * 3.14, user_time=1 + i * 2.718, kernel_time=1 + i * 0.4, cpu_usage=100 + i,
                        memory_usage=314 * (i + 1)))

    variants_of_test_this = m.variants_of('test_this')
    assert len(variants_of_test_this) == 1
    variants_of_test_that = m.variants_of('test_that')
    assert len(variants_of_test_that) == 2


def test_collection_metric_unique(gen):
    m, u = Metrics(), Metrics()
    ch = ['contexthashvalue1', 'contexthashvalue2', 'contexthashvalue3']
    sh = ['sessionsha1value1', 'sessionsha1value2', 'sessionsha1value3']
    for i, (c, s) in enumerate(zip(ch, sh)):
        test_name = 'test_that' if i % 2 == 0 else 'test_this'
        metric = Metric(context_h=c, session_h=s, start_time=f'2020-04-26T{10 + i}:00:52.372833',
                        item_path=f'item.path._{i}', item=test_name, variant=f'{test_name}[{i}]',
                        path=f'/path/to/test/{i}', kind=MetricScope.FUNCTION, component=f'comp_{i}',
                        wall_time=1 + i * 3.14, user_time=1 + i * 2.718, kernel_time=1 + i * 0.4, cpu_usage=100 + i,
                        memory_usage=314 * (i + 1))
        m.append(metric)
        u.append(metric)
    for i, (c, s) in enumerate(zip(ch, sh)):
        test_name = 'test_that' if i % 2 == 0 else 'test_this'
        m.append(Metric(context_h=c, session_h=s, start_time=f'2020-04-26T{10 + i}:00:52.372833',
                        item_path=f'item.path._{i}', item=test_name, variant=f'{test_name}[{i}]',
                        path=f'/path/to/test/{i}', kind=MetricScope.FUNCTION, component=f'comp_{i}',
                        wall_time=1 + i * 3.14, user_time=1 + i * 2.718, kernel_time=1 + i * 0.4, cpu_usage=100 + i,
                        memory_usage=314 * (i + 1)))

    assert u == m.unique()
    m.unique(inplace=True)
    assert u == m
