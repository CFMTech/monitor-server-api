# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from monitor_api.enums import ResourceMethod, ResourceType
from monitor_api.monitor import Monitor, MetricScope
from monitor_api.core.collections import Sessions, Contexts
import datetime
import collections
import itertools


def test_no_db():
    m = Monitor('/tmp/my.db')
    assert m.count_components() == -1
    assert m.count_contexts() == -1
    assert m.count_sessions() == -1
    assert m.count_metrics() == -1
    assert m.count_metrics(session_h='17d1ed00eb13760023d4b21e70ad01aa') == -1
    assert m.count_metrics(context_h='28dae49c83587322a3b535612add39e3') == -1
    assert m.count_metrics(scm_ref='984cefd4b0032a8b736e2f2d5fac8abef0df8cda') == -1
    assert not m.list_components()
    assert not m.list_metrics()
    assert not m.list_contexts()
    assert not m.list_sessions()
    assert not m.list_pipelines()
    assert not m.list_component_pipelines('math.prime')
    assert not m.list_pipeline_builds('master-py36')
    assert not m.list_component_pipeline_builds('math.prime', 'master-py36')
    assert not m.list_item_metrics('test_prime')
    assert not m.list_context_metrics('9ae6c23d7c6b4562393385edf6da8500')
    assert not m.list_metrics_by_scm_id('dc22efdde931451134b8922d93512d288460bba5')
    assert not m.list_session_metrics('86a17d881a4458e3bb273c688f6a9fe0')
    assert m.get_session('86a17d881a4458e3bb273c688f6a9fe0') is None
    assert not m.list_component_metrics('math.prime')
    assert not m.list_metrics_of_variant('test_prime[2]')
    assert not m.list_metrics_of_variant('test_prime[2]', 'math.prime')
    assert m.get_context('9ae6c23d7c6b4562393385edf6da8500') is None
    assert not m.list_metrics_by_type(MetricScope.FUNCTION)
    assert not m.list_metrics_by_type(MetricScope.MODULE)
    assert not m.list_metrics_by_type(MetricScope.PACKAGE)
    assert not m.list_metrics_from_pattern(item='test_prime[1')
    assert not m.list_metrics_from_pattern(variant='test_prime[1')
    for rt, rm in itertools.product((_rt for _rt in ResourceType), (_rm for _rm in ResourceMethod)):
        assert not m.list_metrics_resources(rt, rm, 5)
        assert not m.list_metrics_resources_from_component('math.prime', rt, rm, 5)
        assert not m.list_metrics_resources_from_pipeline('master-py38', rt, rm, 5)
        assert not m.list_metrics_resources_from_build('master-py38', '4', rt, rm, 5)
    assert not m.list_build_sessions('master-py36', '4')


def test_db_no_values(monitor_db_no_data):
    assert monitor_db_no_data.count_components() == 0
    assert monitor_db_no_data.count_contexts() == 0
    assert monitor_db_no_data.count_sessions() == -0
    assert monitor_db_no_data.count_metrics() == 0
    assert monitor_db_no_data.count_metrics(session_h='17d1ed00eb13760023d4b21e70ad01aa') == 0
    assert monitor_db_no_data.count_metrics(context_h='28dae49c83587322a3b535612add39e3') == 0
    assert monitor_db_no_data.count_metrics(scm_ref='984cefd4b0032a8b736e2f2d5fac8abef0df8cda') == 0
    assert not monitor_db_no_data.list_components()
    assert not monitor_db_no_data.list_metrics()
    assert not monitor_db_no_data.list_contexts()
    assert not monitor_db_no_data.list_sessions()
    assert not monitor_db_no_data.list_pipelines()
    assert not monitor_db_no_data.list_component_pipelines('math.prime')
    assert not monitor_db_no_data.list_pipeline_builds('master-py36')
    assert not monitor_db_no_data.list_component_pipeline_builds('math.prime', 'master-py36')
    assert not monitor_db_no_data.list_item_metrics('test_prime')
    assert not monitor_db_no_data.list_context_metrics('9ae6c23d7c6b4562393385edf6da8500')
    assert not monitor_db_no_data.list_metrics_by_scm_id('dc22efdde931451134b8922d93512d288460bba5')
    assert not monitor_db_no_data.list_session_metrics('86a17d881a4458e3bb273c688f6a9fe0')
    assert monitor_db_no_data.get_session('86a17d881a4458e3bb273c688f6a9fe0') is None
    assert not monitor_db_no_data.list_component_metrics('math.prime')
    assert not monitor_db_no_data.list_metrics_of_variant('test_prime[2]')
    assert not monitor_db_no_data.list_metrics_of_variant('test_prime[2]', 'math.prime')
    assert monitor_db_no_data.get_context('9ae6c23d7c6b4562393385edf6da8500') is None
    assert not monitor_db_no_data.list_metrics_by_type(MetricScope.FUNCTION)
    assert not monitor_db_no_data.list_metrics_by_type(MetricScope.MODULE)
    assert not monitor_db_no_data.list_metrics_by_type(MetricScope.PACKAGE)
    assert not monitor_db_no_data.list_metrics_from_pattern(item='test_prime[1')
    assert not monitor_db_no_data.list_metrics_from_pattern(variant='test_prime[1')
    for rt, rm in itertools.product((_rt for _rt in ResourceType), (_rm for _rm in ResourceMethod)):
        assert not monitor_db_no_data.list_metrics_resources(rt, rm, 5)
        assert not monitor_db_no_data.list_metrics_resources_from_component('math.prime', rt, rm, 5)
        assert not monitor_db_no_data.list_metrics_resources_from_pipeline('master-py38', rt, rm, 5)
        assert not monitor_db_no_data.list_metrics_resources_from_build('master-py38', '4', rt, rm, 5)
    assert not monitor_db_no_data.list_build_sessions('master-py36', '4')


def test_entities_count(monitor_db):
    assert monitor_db.count_sessions() == 20
    assert monitor_db.count_components() == 3
    assert monitor_db.count_contexts() == 2
    assert monitor_db.count_metrics() == 260
    assert monitor_db.count_metrics(session_h='17d1ed00eb13760023d4b21e70ad01aa') == 13
    assert monitor_db.count_metrics(context_h='28dae49c83587322a3b535612add39e3') == 130
    assert monitor_db.count_metrics(scm_ref='984cefd4b0032a8b736e2f2d5fac8abef0df8cda') == 52


def test_count_metrics_of_single_session(monitor_db):
    assert monitor_db.count_metrics('b572200744a298a365bbbd1a8bb0cd21') == 13


def test_count_metrics_of_unknown_session(monitor_db):
    assert monitor_db.count_metrics('babc200744a298a365bbbd1a8bb0cd21') == 0


def test_list_components(monitor_db):
    components = monitor_db.list_components()
    assert ['math.analytics', 'math.distance', 'math.prime'] == components


def test_list_sessions(monitor_db):
    sessions = monitor_db.list_sessions()
    assert len(sessions) == 20
    assert 'b572200744a298a365bbbd1a8bb0cd21' in sessions
    assert 'b556200744a298a365bbbd1a8bb0cd21' not in sessions

    sessions = monitor_db.list_sessions(with_tags=['version', 'numpy', 'python'],
                                        restrict_flags=["1.1.0", "1.18.5"],
                                        method="match_all")
    assert len(sessions) == 2
    for session in sessions.values():
        assert session.tags['version'] == "1.1.0"
        assert session.tags['numpy'] == "1.18.5"


def test_list_contexts(monitor_db):
    contexts = monitor_db.list_contexts()
    assert len(contexts) == 2
    assert '28dae49c83587322a3b535612add39e3' in contexts
    assert '9ae6c23d7c6b4562393385edf6da8500' in contexts


def test_list_metrics(monitor_db):
    metrics = monitor_db.list_metrics()
    assert len(metrics) == 260


def test_list_pipelines(monitor_db):
    pipelines = monitor_db.list_pipelines()
    assert len(pipelines) == 2
    for pipeline in ["master-py36", "master-py38"]:
        assert pipeline in pipelines


def test_list_pipeline_builds(monitor_db):
    builds = monitor_db.list_pipeline_builds("master-py36")
    assert len(builds) == 10
    assert [int(i) for i in builds] == [i for i in range(1, 11)]


def test_list_component_pipelines(monitor_db):
    pipelines = monitor_db.list_component_pipelines('math.prime')
    assert len(pipelines) == 2
    for pipeline in ["master-py36", "master-py38"]:
        assert pipeline in pipelines


def test_list_component_pipeline_builds(monitor_db):
    builds = monitor_db.list_component_pipeline_builds('math.prime', "master-py36")
    assert len(builds) == 10
    assert [int(i) for i in builds] == [i for i in range(1, 11)]


def test_get_metrics(monitor_db):
    metrics = monitor_db.list_item_metrics('test_prime')
    assert len(metrics) == 100
    variants = collections.Counter((metric.variant for metric in metrics))
    for metric in metrics:
        assert metric.item == 'test_prime'
    for variant in variants:
        assert variants[variant] == 20


def test_metrics_with_context(monitor_db):
    metrics = monitor_db.list_context_metrics('9ae6c23d7c6b4562393385edf6da8500')
    assert len(metrics) == 130
    for metric in metrics:
        assert metric.context == '9ae6c23d7c6b4562393385edf6da8500'


def test_metrics_with_session(monitor_db):
    metrics = monitor_db.list_session_metrics('86a17d881a4458e3bb273c688f6a9fe0')
    assert len(metrics) == 13
    for metric in metrics:
        assert metric.session == '86a17d881a4458e3bb273c688f6a9fe0'


def test_metrics_by_scm_id(monitor_db):
    metrics = monitor_db.list_metrics_by_scm_id('dc22efdde931451134b8922d93512d288460bba5')
    assert len(metrics) == 52
    d_session = dict()
    for metric in metrics:
        if metric.session not in d_session:
            d_session[metric.session] = 0
        d_session[metric.session] += 1
        assert metric.session in ['86a17d881a4458e3bb273c688f6a9fe0', 'b572200744a298a365bbbd1a8bb0cd21',
                                  'f087cfd87da1c3ca1f5da94a90627d9c', 'c9dd28cd8bb77f420a00dd229cc87f53']
    for session in ['86a17d881a4458e3bb273c688f6a9fe0', 'b572200744a298a365bbbd1a8bb0cd21',
                    'f087cfd87da1c3ca1f5da94a90627d9c', 'c9dd28cd8bb77f420a00dd229cc87f53']:
        assert d_session[session] == 13


def test_get_session_details(monitor_db):
    s = monitor_db.get_session('86a17d881a4458e3bb273c688f6a9fe0')
    assert s.h == '86a17d881a4458e3bb273c688f6a9fe0'
    assert s.scm == 'dc22efdde931451134b8922d93512d288460bba5'
    assert s.start_date == datetime.datetime(2021, 2, 9, 12, 12, 4, 136861)
    assert s.tags == dict(pipeline_branch="master-py36", pipeline_build_no="6", __ci__="circleci",
                          version="1.0.0", numpy="1.18.5", python="3.6", origin="conda-forge")


def test_metric_by_component(monitor_db):
    m = monitor_db.list_component_metrics('math.prime')
    assert len(m) == 200
    for metric in m:
        assert metric.component == 'math.prime'


def test_metric_variant(monitor_db):
    m = monitor_db.list_metrics_of_variant('test_prime[2]')
    assert len(m) == 20
    for metric in m:
        assert metric.item == 'test_prime'
        assert metric.variant == 'test_prime[2]'

    m = monitor_db.list_metrics_of_variant('test_prime[2]', 'math.prime')
    assert len(m) == 20
    for metric in m:
        assert metric.item == 'test_prime'
        assert metric.variant == 'test_prime[2]'

    m = monitor_db.list_metrics_of_variant('test_prime[2]', 'math.distance')
    assert not len(m)


def test_get_context(monitor_db):
    c = monitor_db.get_context('9ae6c23d7c6b4562393385edf6da8500')
    assert c.cpu_count == 8
    assert c.cpu_freq == 2500
    assert c.cpu_type == 'i386'
    assert c.cpu_vendor == 'Intel(R) Core(TM) i7-4870HQ CPU @ 2.50GHz'
    assert c.total_ram == 16384
    assert c.machine_node == 'Rotondu.local'
    assert c.machine_type == 'x86_64'
    assert c.machine_arch == '64bit'
    assert c.sys_info == 'Darwin - 18.7.0'
    assert c.python_info == '3.6.12 | packaged by conda-forge | (default, Dec  9 2020, 00:24:39) [GCC Clang 11.0.0]'

    assert monitor_db.get_context('do not exists') is None


def test_metric_by_type(monitor_db):
    metrics = monitor_db.list_metrics_by_type(MetricScope.FUNCTION)
    assert len(metrics) == 260
    for metric in metrics:
        assert metric.scope == MetricScope.FUNCTION

    metrics = monitor_db.list_metrics_by_type(MetricScope.MODULE)
    assert not len(metrics)
    for metric in metrics:
        assert metric.scope == MetricScope.MODULE

    metrics = monitor_db.list_metrics_by_type(MetricScope.PACKAGE)
    assert not len(metrics)
    for metric in metrics:
        assert metric.scope == MetricScope.PACKAGE


def test_metric_by_pattern(monitor_db):
    metrics = monitor_db.list_metrics_from_pattern(variant='test_prime[1')
    assert len(metrics) == 20
    for metric in metrics:
        assert metric.variant.startswith('test_prime[1')

    metrics = monitor_db.list_metrics_from_pattern(variant='not a variant')
    assert not metrics

    metrics = monitor_db.list_metrics_from_pattern(item='test_p')
    assert len(metrics) == 100
    for metric in metrics:
        assert metric.item.startswith('test_p')

    metrics = monitor_db.list_metrics_from_pattern(item='not a test')
    assert not metrics

    metrics = monitor_db.list_metrics_from_pattern()
    assert metrics is not None
    assert not len(metrics)


def test_get_metrics_from_resources(monitor_db):
    metrics = monitor_db.list_metrics_resources(ResourceType.MEMORY,  ResourceMethod.TOP, 15)

    got = [(metric.variant, int(metric.memory_usage)) for metric in metrics]
    exp = [('test_prime[982451653]', 12538), ('test_prime[982451653]', 12334),
           ('test_prime[982451653]', 11774), ('test_prime[982451653]', 11710),
           ('test_not_prime[524029229]', 8038), ('test_not_prime[524029229]', 8038),
           ('test_not_prime[524029229]', 8033), ('test_not_prime[524029229]', 8031),
           ('test_prime[982451653]', 982), ('test_prime[982451653]', 982), ('test_prime[982451653]', 981),
           ('test_prime[982451653]', 979), ('test_not_prime[524029229]', 545),
           ('test_not_prime[524029229]', 544), ('test_not_prime[524029229]', 544)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources(ResourceType.MEMORY,  ResourceMethod.LOWEST, 10)
    got = [(metric.variant, int(metric.memory_usage)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 27),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 27),
           ('test_levenshtein', 27), ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 27),
           ('test_prime[2]', 27), ('test_prime[3]', 27), ('test_prime[997]', 27), ('test_prime[104743]', 27),
           ('test_prime[982451653]', 27), ('test_not_prime[25]', 27)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources(ResourceType.CPU,  ResourceMethod.TOP, 15)
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 213),
           ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 203),
           ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 193),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 158),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 152),
           ('test_levenshtein', 99),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 99),
           ('test_prime[982451653]', 99),
           ('test_prime[982451653]', 99),
           ('test_prime[982451653]', 99),
           ('test_not_prime[524029229]', 99),
           ('test_prime[982451653]', 99),
           ('test_not_prime[524029229]', 99),
           ('test_levenshtein', 99),
           ('test_not_prime[524029229]', 99)]

    got = [(metric.variant, int(metric.cpu_usage * 100)) for metric in metrics]
    assert got == exp

    metrics = monitor_db.list_metrics_resources(ResourceType.CPU,  ResourceMethod.LOWEST, 15)
    got = [(metric.variant, int(metric.cpu_usage * 100)) for metric in metrics]
    exp = [('test_not_prime[25]', 1), ('test_not_prime[25]', 2), ('test_not_prime[39]', 2),
           ('test_not_prime[39]', 2), ('test_prime[2]', 2), ('test_not_prime[1023]', 2),
           ('test_not_prime[39]', 2), ('test_not_prime[100697]', 2), ('test_prime[3]', 2),
           ('test_prime[104743]', 2), ('test_not_prime[39]', 2), ('test_prime[104743]', 2),
           ('test_not_prime[39]', 2), ('test_not_prime[1023]', 2), ('test_prime[2]', 2)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources(ResourceType.KERNEL_TIME,  ResourceMethod.LOWEST, 15)
    got = [(metric.variant, int(metric.kernel_time * 1000)) for metric in metrics]
    exp = [('test_prime[104743]', 2), ('test_not_prime[100697]', 2), ('test_not_prime[1023]', 2),
           ('test_prime[3]', 2), ('test_prime[997]', 2), ('test_not_prime[39]', 2),
           ('test_not_prime[1023]', 2), ('test_not_prime[1023]', 2), ('test_prime[3]', 2),
           ('test_prime[997]', 2), ('test_prime[2]', 2), ('test_prime[3]', 2),
           ('test_not_prime[524029229]', 2), ('test_prime[3]', 2), ('test_prime[982451653]', 2)]
    assert got == exp
    metrics = monitor_db.list_metrics_resources(ResourceType.KERNEL_TIME,  ResourceMethod.TOP, 15)
    got = [(metric.variant, int(metric.kernel_time * 100)) for metric in metrics]
    exp = [('test_prime[982451653]', 1213), ('test_prime[982451653]', 1012), ('test_prime[982451653]', 885),
           ('test_prime[982451653]', 772), ('test_levenshtein', 515), ('test_not_prime[524029229]', 352),
           ('test_not_prime[524029229]', 352), ('test_not_prime[524029229]', 234),
           ('test_not_prime[524029229]', 233), ('test_prime[982451653]', 211), ('test_levenshtein', 189),
           ('test_prime[982451653]', 145), ('test_levenshtein', 114), ('test_not_prime[524029229]', 101),
           ('test_not_prime[524029229]', 69)]
    assert got == exp
    metrics = monitor_db.list_metrics_resources(ResourceType.USER_TIME,  ResourceMethod.LOWEST, 15)
    got = [(metric.variant, int(metric.kernel_time * 1000)) for metric in metrics]
    exp = [('test_prime[104743]', 2), ('test_prime[3]', 2), ('test_not_prime[1023]', 2), ('test_not_prime[100697]', 2),
           ('test_not_prime[39]', 2), ('test_prime[2]', 2), ('test_prime[3]', 2), ('test_prime[2]', 3),
           ('test_not_prime[1023]', 2), ('test_not_prime[39]', 2), ('test_not_prime[1023]', 2), ('test_prime[2]', 2),
           ('test_prime[997]', 2), ('test_not_prime[25]', 2), ('test_prime[2]', 2)]
    assert got == exp
    metrics = monitor_db.list_metrics_resources(ResourceType.USER_TIME,  ResourceMethod.TOP, 15)
    got = [(metric.variant, int(metric.kernel_time * 100)) for metric in metrics]
    exp = [('test_levenshtein', 515), ('test_levenshtein', 114), ('test_levenshtein', 189), ('test_levenshtein', 17),
           ('test_prime[982451653]', 1213), ('test_prime[982451653]', 885), ('test_prime[982451653]', 772),
           ('test_prime[982451653]', 1012), ('test_prime[982451653]', 211), ('test_prime[982451653]', 145),
           ('test_prime[982451653]', 33), ('test_not_prime[524029229]', 352), ('test_not_prime[524029229]', 352),
           ('test_prime[982451653]', 33), ('test_not_prime[524029229]', 233)]
    assert got == exp
    metrics = monitor_db.list_metrics_resources(ResourceType.TOTAL_TIME,  ResourceMethod.LOWEST, 15)
    got = [(metric.variant, int(metric.kernel_time * 1000)) for metric in metrics]
    exp = [('test_prime[104743]', 2), ('test_prime[3]', 2), ('test_not_prime[1023]', 2), ('test_not_prime[100697]', 2),
           ('test_not_prime[1023]', 2), ('test_not_prime[39]', 2), ('test_prime[3]', 2), ('test_prime[997]', 2),
           ('test_prime[2]', 2), ('test_prime[997]', 2), ('test_not_prime[1023]', 2), ('test_not_prime[524029229]', 2),
           ('test_prime[997]', 2), ('test_prime[2]', 2), ('test_prime[2]', 2)]
    assert got == exp
    metrics = monitor_db.list_metrics_resources(ResourceType.TOTAL_TIME,  ResourceMethod.TOP, 15)
    got = [(metric.variant, int(metric.kernel_time * 100)) for metric in metrics]
    exp = [('test_not_prime[524029229]', 234), ('test_levenshtein', 515), ('test_levenshtein', 114),
           ('test_levenshtein', 189), ('test_levenshtein', 17), ('test_prime[982451653]', 1213),
           ('test_prime[982451653]', 885), ('test_prime[982451653]', 772), ('test_prime[982451653]', 1012),
           ('test_prime[982451653]', 211), ('test_prime[982451653]', 145), ('test_prime[982451653]', 33),
           ('test_not_prime[524029229]', 352), ('test_not_prime[524029229]', 352), ('test_prime[982451653]', 33)]
    assert got == exp


def test_get_metrics_resource_from_component(monitor_db):
    component = 'math.prime'
    metrics = monitor_db.list_metrics_resources_from_component(component, ResourceType.MEMORY,  ResourceMethod.TOP, 5)

    got = [(metric.variant, int(metric.memory_usage)) for metric in metrics]
    exp = [('test_prime[982451653]', 12538), ('test_prime[982451653]', 12334),
           ('test_prime[982451653]', 11774), ('test_prime[982451653]', 11710),
           ('test_not_prime[524029229]', 8038)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_component(component, ResourceType.MEMORY,
                                                               ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.memory_usage)) for metric in metrics]
    exp = [('test_prime[2]', 27), ('test_prime[3]', 27), ('test_prime[997]', 27),
           ('test_prime[104743]', 27), ('test_prime[982451653]', 27)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_component(component, ResourceType.CPU,
                                                               ResourceMethod.TOP, 5)
    exp = [('test_prime[982451653]', 99), ('test_prime[982451653]', 99), ('test_prime[982451653]', 99),
           ('test_not_prime[524029229]', 99), ('test_prime[982451653]', 99)]
    got = [(metric.variant, int(metric.cpu_usage * 100)) for metric in metrics]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_component(component, ResourceType.CPU,
                                                               ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.cpu_usage * 100)) for metric in metrics]
    exp = [('test_not_prime[25]', 1), ('test_not_prime[25]', 2), ('test_not_prime[39]', 2),
           ('test_not_prime[39]', 2), ('test_prime[2]', 2)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_component(component, ResourceType.KERNEL_TIME,
                                                               ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.kernel_time * 1000)) for metric in metrics]
    exp = [('test_prime[104743]', 2), ('test_not_prime[100697]', 2),
           ('test_not_prime[1023]', 2), ('test_prime[3]', 2), ('test_prime[997]', 2)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_component(component, ResourceType.KERNEL_TIME,
                                                               ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.kernel_time * 100)) for metric in metrics]
    exp = [('test_prime[982451653]', 1213), ('test_prime[982451653]', 1012), ('test_prime[982451653]', 885),
           ('test_prime[982451653]', 772), ('test_not_prime[524029229]', 352)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_component(component, ResourceType.USER_TIME,
                                                               ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.kernel_time * 1000)) for metric in metrics]
    exp = [('test_prime[104743]', 2), ('test_prime[3]', 2), ('test_not_prime[1023]', 2), ('test_not_prime[100697]', 2),
           ('test_not_prime[39]', 2)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_component(component, ResourceType.USER_TIME,
                                                               ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.kernel_time * 100)) for metric in metrics]
    exp = [('test_prime[982451653]', 1213), ('test_prime[982451653]', 885), ('test_prime[982451653]', 772),
           ('test_prime[982451653]', 1012), ('test_prime[982451653]', 211)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_component(component, ResourceType.TOTAL_TIME,
                                                               ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.kernel_time * 1000)) for metric in metrics]
    exp = [('test_prime[104743]', 2), ('test_prime[3]', 2), ('test_not_prime[1023]', 2),
           ('test_not_prime[100697]', 2), ('test_not_prime[1023]', 2)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_component(component, ResourceType.TOTAL_TIME,
                                                               ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.kernel_time * 100)) for metric in metrics]
    exp = [('test_not_prime[524029229]', 234), ('test_prime[982451653]', 1213),
           ('test_prime[982451653]', 885), ('test_prime[982451653]', 772), ('test_prime[982451653]', 1012)]
    assert got == exp


def test_list_metrics_resources_from_pipeline(monitor_db):
    pipeline = 'master-py38'
    metrics = monitor_db.list_metrics_resources_from_pipeline(pipeline, ResourceType.MEMORY,
                                                              ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.memory_usage)) for metric in metrics]
    exp = [('test_prime[982451653]', 12538), ('test_prime[982451653]', 12334), ('test_not_prime[524029229]', 8038),
           ('test_not_prime[524029229]', 8033), ('test_prime[982451653]', 982)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_pipeline(pipeline, ResourceType.CPU,
                                                              ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.cpu_usage * 100)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 193), ('test_levenshtein', 99),
           ('test_prime[982451653]', 99), ('test_prime[982451653]', 99), ('test_not_prime[524029229]', 99)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_pipeline(pipeline, ResourceType.KERNEL_TIME,
                                                              ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.kernel_time * 1000)) for metric in metrics]
    exp = [('test_prime[982451653]', 8856), ('test_prime[982451653]', 7723), ('test_not_prime[524029229]', 2342),
           ('test_not_prime[524029229]', 2339), ('test_levenshtein', 1895)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_pipeline(pipeline, ResourceType.USER_TIME,
                                                              ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.user_time * 1000)) for metric in metrics]
    exp = [('test_levenshtein', 644435), ('test_levenshtein', 635866), ('test_prime[982451653]', 417068),
           ('test_prime[982451653]', 411321), ('test_prime[982451653]', 240034)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_pipeline(pipeline, ResourceType.TOTAL_TIME,
                                                              ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.wall_time * 100)) for metric in metrics]
    exp = [('test_not_prime[524029229]', 91806), ('test_levenshtein', 64828), ('test_levenshtein', 63625),
           ('test_prime[982451653]', 42797), ('test_prime[982451653]', 42009)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_pipeline(pipeline, ResourceType.MEMORY,
                                                              ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.memory_usage)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 29),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 29),
           ('test_levenshtein', 29), ('test_prime[2]', 29), ('test_prime[3]', 29)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_pipeline(pipeline, ResourceType.CPU,
                                                              ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.cpu_usage * 100)) for metric in metrics]
    exp = [('test_not_prime[25]', 1), ('test_not_prime[25]', 2), ('test_not_prime[39]', 2),
           ('test_not_prime[39]', 2), ('test_prime[2]', 2)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_pipeline(pipeline, ResourceType.KERNEL_TIME,
                                                              ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.kernel_time * 100)) for metric in metrics]
    exp = [('test_prime[997]', 0), ('test_not_prime[39]', 0), ('test_not_prime[1023]', 0),
           ('test_levenshtein', 0), ('test_not_prime[1023]', 0)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_pipeline(pipeline, ResourceType.USER_TIME,
                                                              ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.user_time * 100)) for metric in metrics]
    exp = [('test_not_prime[39]', 0), ('test_prime[2]', 0), ('test_prime[104743]', 0),
           ('test_not_prime[100697]', 0), ('test_prime[2]', 0)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_pipeline(pipeline, ResourceType.TOTAL_TIME,
                                                              ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.wall_time * 100)) for metric in metrics]
    exp = [('test_prime[997]', 18), ('test_prime[997]', 18), ('test_prime[2]', 18),
           ('test_not_prime[25]', 18), ('test_levenshtein', 18)]
    assert got == exp


def test_list_metrics_resources_from_build(monitor_db):
    pipeline = 'master-py38'
    build = "4"
    metrics = monitor_db.list_metrics_resources_from_build(pipeline, build, ResourceType.MEMORY,
                                                           ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.memory_usage)) for metric in metrics]
    exp = [('test_prime[982451653]', 12334), ('test_not_prime[524029229]', 8033), ('test_prime[104743]', 46),
           ('test_prime[997]', 44), ('test_prime[3]', 44)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_build(pipeline, build, ResourceType.CPU,
                                                           ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.cpu_usage * 100)) for metric in metrics]
    exp = [('test_not_prime[524029229]', 99), ('test_prime[982451653]', 99),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 16),
           ('test_prime[104743]', 12), ('test_not_prime[100697]', 11)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_build(pipeline, build, ResourceType.KERNEL_TIME,
                                                           ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.kernel_time * 1000)) for metric in metrics]
    exp = [('test_prime[982451653]', 8856), ('test_not_prime[524029229]', 2339),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 7),
           ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 4), ('test_not_prime[100697]', 3)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_build(pipeline, build, ResourceType.USER_TIME,
                                                           ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.user_time * 1000)) for metric in metrics]
    exp = [('test_prime[982451653]', 417068), ('test_not_prime[524029229]', 209410),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 34),
           ('test_prime[104743]', 25), ('test_not_prime[100697]', 24)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_build(pipeline, build, ResourceType.TOTAL_TIME,
                                                           ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.wall_time * 100)) for metric in metrics]
    exp = [('test_prime[982451653]', 42797), ('test_not_prime[524029229]', 21207), ('test_not_prime[25]', 26),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 24), ('test_not_prime[100697]', 23)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_build(pipeline, build, ResourceType.MEMORY,
                                                           ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.memory_usage)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 30), ('test_not_prime[25]', 36),
           ('test_not_prime[39]', 36), ('test_not_prime[1023]', 36), ('test_not_prime[100697]', 37)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_build(pipeline, build, ResourceType.CPU,
                                                           ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.cpu_usage * 100)) for metric in metrics]
    exp = [('test_not_prime[25]', 1), ('test_not_prime[39]', 2), ('test_not_prime[1023]', 2),
           ('test_prime[3]', 2), ('test_levenshtein', 2)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_build(pipeline, build, ResourceType.KERNEL_TIME,
                                                           ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.kernel_time * 100)) for metric in metrics]
    exp = [('test_not_prime[39]', 0), ('test_levenshtein', 0), ('test_not_prime[1023]', 0),
           ('test_not_prime[25]', 0), ('test_prime[997]', 0)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_build(pipeline, build, ResourceType.USER_TIME,
                                                           ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.user_time * 100)) for metric in metrics]
    exp = [('test_not_prime[39]', 0), ('test_prime[3]', 0), ('test_prime[2]', 0),
           ('test_not_prime[25]', 0), ('test_levenshtein', 0)]
    assert got == exp

    metrics = monitor_db.list_metrics_resources_from_build(pipeline, build, ResourceType.TOTAL_TIME,
                                                           ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.wall_time * 100)) for metric in metrics]
    exp = [('test_levenshtein', 20), ('test_not_prime[39]', 20), ('test_prime[2]', 20),
           ('test_prime[997]', 20), ('test_prime[3]', 20)]
    assert got == exp


def test_get_metrics_from_sessions(monitor_db):
    sessions = Sessions()
    session = sessions.add(monitor_db.get_session('b83742056ad0ed304d821562b7c209ff'))
    metrics_from_session = monitor_db.list_metrics_from(sessions=sessions)
    for metric in metrics_from_session:
        assert metric.session == session.h
    all_metrics = monitor_db.list_metrics()
    metric_from_session_count = sum(1 for metric in all_metrics if metric.session == session.h)
    assert metric_from_session_count == len(metrics_from_session)


def test_get_metrics_from_context(monitor_db):
    contexts = Contexts()
    context = contexts.add(monitor_db.get_context('9ae6c23d7c6b4562393385edf6da8500'))
    metrics_from_context = monitor_db.list_metrics_from(contexts=contexts)
    for metric in metrics_from_context:
        assert metric.context == context.h
    all_metrics = monitor_db.list_metrics()
    metric_from_context_count = sum(1 for metric in all_metrics if metric.context == context.h)
    assert metric_from_context_count == len(metrics_from_context)


def test_get_metrics_from_session_context(monitor_db):
    # We voluntary get a session linked to the context
    sessions, contexts = Sessions(), Contexts()
    session = sessions.add(monitor_db.get_session('7768124332f353446557878a89ef6f4c'))
    context = contexts.add(monitor_db.get_context('28dae49c83587322a3b535612add39e3'))

    metrics_from = monitor_db.list_metrics_from(sessions=sessions, contexts=contexts)
    for metric in metrics_from:
        assert metric.context == context.h or metric.session == session.h
    all_metrics = monitor_db.list_metrics()
    valid_metric_count = sum(1 for m in all_metrics if m.context == context.h or m.session == session.h)
    assert valid_metric_count == len(metrics_from.unique())


def test_get_sessions_from_metrics(monitor_db):
    contexts = Contexts()
    context = contexts.add(monitor_db.get_context('28dae49c83587322a3b535612add39e3'))
    metrics = monitor_db.list_metrics_from(contexts=contexts)
    sessions = monitor_db.list_sessions_from(metrics)
    assert len(sessions) == 10
    # The other way around
    metrics = monitor_db.list_metrics_from(sessions=sessions)
    for metric in metrics:
        assert metric.context == context.h


def test_get_contexts_from_metrics(monitor_db):
    sessions = Sessions()
    sessions.add(monitor_db.get_session('7768124332f353446557878a89ef6f4c'))
    metrics = monitor_db.list_metrics_from(sessions=sessions)
    contexts = monitor_db.list_contexts_from(metrics)
    assert len(contexts) == 1
    # The other way around
    metrics = monitor_db.list_metrics_from(contexts=contexts)
    ctxs = [ctx.h for ctx in contexts.values()]
    for metric in metrics:
        assert metric.context in ctxs


def test_get_sessions_from_build(monitor_db):
    sessions = monitor_db.list_build_sessions('master-py36', '4')
    assert len(sessions) == 1
    for session in sessions.values():
        assert session.tags['pipeline_branch'] == 'master-py36'
        assert session.tags['pipeline_build_no'] == '4'
