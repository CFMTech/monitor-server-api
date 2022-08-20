# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from monitor_api.enums import Field, MetricScope
from monitor_api.core.entities import Context, Metric, Session
import datetime
import pytest


def test_entity_session_basic(gen):
    h, scm = gen.random_string(26), gen.random_string(32)
    s = Session(h=h, scm_ref=scm, run_date='2020-04-26T23:00:52.372833',
                tags=dict(build_no='123', build_branch='pipeline'))
    assert s.h == h
    assert s.scm == scm
    assert s.tags == dict(build_no="123", build_branch='pipeline')
    assert s.start_date == datetime.datetime.fromisoformat('2020-04-26T23:00:52.372833')
    s = Session(h=h, scm_ref=scm, run_date='2020-04-26T23:00:52.372833',
                tags=[dict(build_no='123', build_branch='pipeline')])
    assert s.h == h
    assert s.scm == scm
    assert s.tags == dict()
    assert s.start_date == datetime.datetime.fromisoformat('2020-04-26T23:00:52.372833')
    s = Session(h=h, scm_ref=scm, run_date='2020-04-26T23:00:52.372833',
                tags=[dict(name='build_no', value='123'), dict(name='build_branch', value='pipeline')])
    assert s.h == h
    assert s.scm == scm
    assert s.tags == dict(build_no="123", build_branch='pipeline')
    assert s.start_date == datetime.datetime.fromisoformat('2020-04-26T23:00:52.372833')


def test_entity_session_str(gen):
    h, scm = gen.random_string(26), gen.random_string(32)
    s = Session(h=h, scm_ref=scm, run_date='2020-04-26T23:00:52.372833', tags=None)
    exp = f'{h}:\n    run_date: 2020-04-26 23:00:52.372833\n    scm: {scm}\n'
    assert str(s) == exp
    s = Session(h=h, scm_ref=scm, run_date='2020-04-26T23:00:52.372833',
                tags=dict(build_no='123', build_branch='pipeline'))
    exp = exp + f'    tags:\n        - build_no: 123\n        - build_branch: pipeline\n'
    assert str(s) == exp


def test_entity_session_to_dict(gen):
    h, scm = gen.random_string(26), gen.random_string(32)
    s = Session(h=h, scm_ref=scm, run_date='2020-04-26T23:00:52.372833',
                tags=dict(build_no='123', build_branch='pipeline'))
    assert s.to_dict() == dict(session_h=h, scm=scm, run_date=datetime.datetime.fromisoformat('2020-04-26T23:00:52.372833'),
                               tags=dict(build_no='123', build_branch='pipeline'))
    to_keep = [Field.TAGS, Field.RUN_DATE]
    assert s.to_dict(keep=to_keep) == dict(tags=dict(build_no='123', build_branch='pipeline'),
                                           run_date=datetime.datetime.fromisoformat('2020-04-26T23:00:52.372833'))
    assert s.to_dict(drop=[Field.SESSION_H]) == dict(scm=scm,
                                                     run_date=datetime.datetime.fromisoformat('2020-04-26T23:00:52.372833'),
                                                     tags=dict(build_no='123', build_branch='pipeline'))
    assert s.to_dict(keep=[Field.TAGS], drop=[Field.H]) == dict(tags=dict(build_no='123', build_branch='pipeline'))


def test_entity_metric_basic(gen):
    ch, sh, item = gen.random_string(24), gen.random_string(24), gen.random_string()
    pypath = gen.random_pypath()
    path = gen.random_path()
    variant = item + '[VARIANT1]'
    comp = gen.random_pypath(2)
    m = Metric(context_h=ch, session_h=sh, start_time='2020-04-26T23:00:52.372833', item_path=pypath,
               item=item, variant=variant, path=path, component=comp,
               wall_time=7.23, user_time=4.67, kernel_time=5.34, cpu_usage=134.8, memory_usage=234.56)
    assert m.context == ch
    assert m.session == sh
    assert m.run_time == datetime.datetime.fromisoformat('2020-04-26T23:00:52.372833')
    assert m.item_path == pypath
    assert m.item == item
    assert m.variant == variant
    assert m.path == path
    assert m.scope == MetricScope.FUNCTION
    assert m.component == comp
    assert 7.23 == pytest.approx(m.wall_time)
    assert 4.67 == pytest.approx(m.user_time)
    assert 5.34 == pytest.approx(m.kernel_time)
    assert 134.8 == pytest.approx(m.cpu_usage)
    assert 234.56 == pytest.approx(m.memory_usage)
    assert m.is_function()
    assert not m.is_module()
    assert not m.is_package()
    m = Metric(context_h=ch, session_h=sh, start_time='2020-04-26T23:00:52.372833', item_path=pypath,
               item=item, variant=variant, path=path, component=comp, kind=MetricScope.PACKAGE,
               wall_time=7.23, user_time=4.67, kernel_time=5.34, cpu_usage=134.8, memory_usage=234.56)
    assert not m.is_function()
    assert not m.is_module()
    assert m.is_package()
    m = Metric(context_h=ch, session_h=sh, start_time='2020-04-26T23:00:52.372833', item_path=pypath,
               item=item, variant=variant, path=path, component=comp, kind=MetricScope.MODULE,
               wall_time=7.23, user_time=4.67, kernel_time=5.34, cpu_usage=134.8, memory_usage=234.56)
    assert not m.is_function()
    assert m.is_module()
    assert not m.is_package()
    m = Metric(context_h=ch, session_h=sh, start_time='2020-04-26T23:00:52.372833', item_path=pypath,
               item=item, variant=variant, path=path, component=comp, kind=MetricScope.FUNCTION,
               wall_time=7.23, user_time=4.67, kernel_time=5.34, cpu_usage=134.8, memory_usage=234.56)
    assert m.is_function()
    assert not m.is_module()
    assert not m.is_package()


def test_entity_metric_to_dict(gen):
    ch, sh, item = gen.random_string(24), gen.random_string(24), gen.random_string()
    pypath = gen.random_pypath()
    path = gen.random_path()
    variant = item + '[VARIANT1]'
    comp = gen.random_pypath(2)
    m = Metric(context_h=ch, session_h=sh, start_time='2020-04-26T23:00:52.372833', item_path=pypath,
               item=item, variant=variant, path=path, component=comp, kind=MetricScope.FUNCTION,
               wall_time=7.23, user_time=4.67, kernel_time=5.34, cpu_usage=134.8, memory_usage=234.56)
    exp = dict(context_h=ch, session_h=sh, start_time=datetime.datetime.fromisoformat('2020-04-26T23:00:52.372833'),
               item_path=pypath, item=item, variant=variant, path=path, component=comp, kind='function',
               wall_time=7.23, user_time=4.67, kernel_time=5.34, cpu_usage=134.8, memory_usage=234.56)
    assert m.to_dict() == exp
    for k in ['context_h', 'session_h', 'start_time', 'item_path', 'path', 'kind',
              'wall_time', 'user_time', 'memory_usage']:
        del exp[k]
    assert m.to_dict(keep=[Field.COMPONENT, Field.ITEM, Field.ITEM_VARIANT,
                           Field.CPU_USAGE, Field.KERNEL_TIME]) == exp
    exp = dict(context_h=ch, session_h=sh, start_time=datetime.datetime.fromisoformat('2020-04-26T23:00:52.372833'),
               item_path=pypath, path=path, kind='function',
               wall_time=7.23, user_time=4.67, memory_usage=234.56)
    assert m.to_dict(drop=[Field.COMPONENT, Field.ITEM, Field.ITEM_VARIANT,
                           Field.CPU_USAGE, Field.KERNEL_TIME]) == exp


def test_entity_context_basic(gen):
    h, node = gen.random_string(), gen.random_string()
    mtype, march = gen.random_string(10), gen.random_string(5)
    vendor = 'Intel(R) Core(TM) i7-4870HQ'
    py = '3.8.5 | packaged by conda-forge | (default, Jul 31 2020, 02:18:36) \n[Clang 10.0.1 ]'
    sys = 'Darwin - 18.7.0'
    c = Context(h=h, cpu_count=4, cpu_freq=1000, cpu_type='i386', cpu_vendor=vendor, ram_total=16000,
                mac_node=node, mac_type=mtype, mac_arch=march, sys_info=sys, py_info=py)
    assert c.h == h
    assert c.cpu_count == 4
    assert c.cpu_freq == 1000
    assert c.cpu_type == 'i386'
    assert c.cpu_vendor == vendor
    assert c.total_ram == 16000
    assert c.machine_node == node
    assert c.machine_type == mtype
    assert c.machine_arch == march
    assert c.sys_info == sys
    assert c.python_info == py


def test_entity_context_to_dict(gen):
    h, node = gen.random_string(), gen.random_string()
    mtype, march = gen.random_string(10), gen.random_string(5)
    vendor = 'Intel(R) Core(TM) i7-4870HQ'
    py = '3.8.5 | packaged by conda-forge | (default, Jul 31 2020, 02:18:36) \n[Clang 10.0.1 ]'
    sys = 'Darwin - 18.7.0'
    c = Context(h=h, cpu_count=4, cpu_freq=1000, cpu_type='i386', cpu_vendor=vendor, ram_total=16000,
                mac_node=node, mac_type=mtype, mac_arch=march, sys_info=sys, py_info=py)
    exp = dict(context_h=h, cpu_count=4, cpu_freq=1000, cpu_type='i386', cpu_vendor=vendor, ram=16000,
               hostname=node, type=mtype, arch=march, sys=sys, py=py)
    assert c.to_dict() == exp
    for k in ['cpu_count', 'cpu_type', 'cpu_vendor', 'type', 'arch', 'sys', 'py']:
        del exp[k]
    assert c.to_dict(keep=[Field.MACHINE_NODE, Field.CONTEXT_H,
                           Field.CPU_FREQUENCY_MHZ, Field.RAM_TOTAL_MB]) == exp
    exp = dict(cpu_count=4, cpu_type='i386', cpu_vendor=vendor,
               type=mtype, arch=march, sys=sys, py=py)
    assert c.to_dict(drop=[Field.MACHINE_NODE, Field.CONTEXT_H,
                           Field.CPU_FREQUENCY_MHZ, Field.RAM_TOTAL_MB]) == exp


def test_metric_hashing(gen):
    metric = Metric(context_h='43fd8c62b605beb6db24668a1c51',
                    session_h='c8f2d7bbbbd0fb2b8ddaad9938ad13281380c73e',
                    start_time="2021-02-09T13:49:00.567711",
                    item_path="test_prime",
                    item="test_prime",
                    variant="test_prime[1]",
                    path="spif/Programmation/ptm-demo/tests/test_prime.py",
                    kind=MetricScope.FUNCTION,
                    component="math.prime",
                    wall_time=0.18833708763122559,
                    user_time=0.0024613119999998823,
                    kernel_time=0.003253840000000008,
                    cpu_usage=0.030345334909237173,
                    memory_usage=30.87109375
                    )
    assert metric.hash() == '4cfb6d31f26c0659d3bf663f7a2074e82ce3544036ce8db8f518d72b8a82d224'
