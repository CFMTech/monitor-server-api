# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from monitor_api.enums import MetricScope, ResourceMethod, ResourceType
from monitor_api.core.collections import Sessions, Contexts
import collections
import datetime
import itertools


def test_service_not_up(monitor_service_v1_not_up):
    assert monitor_service_v1_not_up.count_sessions() == -1
    assert monitor_service_v1_not_up.count_components() == -1
    assert monitor_service_v1_not_up.count_contexts() == -1
    assert monitor_service_v1_not_up.count_metrics() == -1
    assert monitor_service_v1_not_up.get_context('28dae49c83587322a3b535612add39e3') is None
    assert monitor_service_v1_not_up.get_session('b83742056ad0ed304d821562b7c209ff') is None
    assert monitor_service_v1_not_up.count_metrics('b572200744a298a365bbbd1a8bb0cd21') == -1
    assert monitor_service_v1_not_up.count_metrics('babc200744a298a365bbbd1a8bb0cd21') == -1
    assert not monitor_service_v1_not_up.list_components()
    assert not monitor_service_v1_not_up.list_sessions()
    assert not monitor_service_v1_not_up.list_contexts()
    assert not monitor_service_v1_not_up.list_metrics()
    assert not monitor_service_v1_not_up.list_context_metrics('28dae49c83587322a3b535612add39e3')
    assert not monitor_service_v1_not_up.list_metrics_by_scm_id('28dae49c83587322a3b535612add39e3')
    for t in [MetricScope.MODULE, MetricScope.FUNCTION, MetricScope.PACKAGE]:
        assert not monitor_service_v1_not_up.list_metrics_by_type(t)
    assert not monitor_service_v1_not_up.list_metrics_from_pattern("an_item", "a_variant")
    assert not monitor_service_v1_not_up.list_metrics_from_pattern("a_variant")
    assert not monitor_service_v1_not_up.list_metrics_from_pattern("an_item")
    assert not monitor_service_v1_not_up.list_pipelines()
    assert not monitor_service_v1_not_up.list_pipeline_builds('a_pipeline')
    assert not monitor_service_v1_not_up.list_session_metrics('b83742056ad0ed304d821562b7c209ff')
    assert not monitor_service_v1_not_up.list_component_metrics('a_component')
    assert not monitor_service_v1_not_up.list_component_pipelines('a_component')
    assert not monitor_service_v1_not_up.list_component_pipeline_builds('a_component', 'a_build')
    assert not monitor_service_v1_not_up.list_item_metrics('an_item')
    assert not monitor_service_v1_not_up.list_metrics_of_variant('a_variant', 'a_component')
    assert not monitor_service_v1_not_up.list_metrics_of_variant('a_variant')
    for rt, rm in itertools.product((_rt for _rt in ResourceType), (_rm for _rm in ResourceMethod)):
        assert not monitor_service_v1_not_up.list_metrics_resources(rt, rm, 5)
        assert not monitor_service_v1_not_up.list_metrics_resources_from_component('math.prime', rt, rm, 5)
        assert not monitor_service_v1_not_up.list_metrics_resources_from_pipeline('master-py38', rt, rm, 5)
        assert not monitor_service_v1_not_up.list_metrics_resources_from_build('master-py38', '4', rt, rm, 5)


def test_service_no_data(monitor_service_v1_no_data):
    assert monitor_service_v1_no_data.count_sessions() == 0
    assert monitor_service_v1_no_data.count_components() == 0
    assert monitor_service_v1_no_data.count_contexts() == 0
    assert monitor_service_v1_no_data.count_metrics() == 0
    assert monitor_service_v1_no_data.get_context('28dae49c83587322a3b535612add39e3') is None
    assert monitor_service_v1_no_data.get_session('b83742056ad0ed304d821562b7c209ff') is None
    assert monitor_service_v1_no_data.count_metrics('b572200744a298a365bbbd1a8bb0cd21') == 0
    assert monitor_service_v1_no_data.count_metrics('babc200744a298a365bbbd1a8bb0cd21') == 0
    assert not monitor_service_v1_no_data.list_components()
    assert not monitor_service_v1_no_data.list_sessions()
    assert not monitor_service_v1_no_data.list_contexts()
    assert not monitor_service_v1_no_data.list_metrics()
    assert not monitor_service_v1_no_data.list_context_metrics('28dae49c83587322a3b535612add39e3')
    assert not monitor_service_v1_no_data.list_metrics_by_scm_id('28dae49c83587322a3b535612add39e3')
    for t in [MetricScope.MODULE, MetricScope.FUNCTION, MetricScope.PACKAGE]:
        assert not monitor_service_v1_no_data.list_metrics_by_type(t)
    assert not monitor_service_v1_no_data.list_metrics_from_pattern("an_item", "a_variant")
    assert not monitor_service_v1_no_data.list_metrics_from_pattern("a_variant")
    assert not monitor_service_v1_no_data.list_metrics_from_pattern("an_item")
    assert not monitor_service_v1_no_data.list_pipelines()
    assert not monitor_service_v1_no_data.list_pipeline_builds('a_pipeline')
    assert not monitor_service_v1_no_data.list_session_metrics('b83742056ad0ed304d821562b7c209ff')
    assert not monitor_service_v1_no_data.list_component_metrics('a_component')
    assert not monitor_service_v1_no_data.list_component_pipelines('a_component')
    assert not monitor_service_v1_no_data.list_component_pipeline_builds('a_component', 'a_build')
    assert not monitor_service_v1_no_data.list_item_metrics('an_item')
    assert not monitor_service_v1_no_data.list_metrics_of_variant('a_variant', 'a_component')
    assert not monitor_service_v1_no_data.list_metrics_of_variant('a_variant')
    for rt, rm in itertools.product((_rt for _rt in ResourceType), (_rm for _rm in ResourceMethod)):
        assert not monitor_service_v1_no_data.list_metrics_resources(rt, rm, 5)
        assert not monitor_service_v1_no_data.list_metrics_resources_from_component('math.prime', rt, rm, 5)
        assert not monitor_service_v1_no_data.list_metrics_resources_from_pipeline('master-py38', rt, rm, 5)
        assert not monitor_service_v1_no_data.list_metrics_resources_from_build('master-py38', '4', rt, rm, 5)


def test_count_entities(monitor_service_v1):
    assert monitor_service_v1.count_sessions() == 20
    assert monitor_service_v1.count_components() == 3
    assert monitor_service_v1.count_contexts() == 2
    assert monitor_service_v1.count_metrics() == 260
    assert monitor_service_v1.count_metrics(session_h='b83742056ad0ed304d821562b7c209ff') == 123
    assert monitor_service_v1.count_metrics(context_h='28dae49c83587322a3b535612add39e3') == 234
    assert monitor_service_v1.count_metrics(scm_ref='babc200744a298a365bbbd1a8bb0cd21') == 345


def test_session_details(monitor_service_v1):
    session = monitor_service_v1.get_session('b83742056ad0ed304d821562b7c209ff')
    assert session.h == 'b83742056ad0ed304d821562b7c209ff'
    assert session.scm == '4c3b3ca9e975a0a5eacd5d802d03c4ba690e8e41'
    assert session.start_date == datetime.datetime(2021, 2, 9, 13, 48, 58, 923094)
    assert session.tags == dict(pipeline_branch="master-py38", pipeline_build_no="10", __ci__="circleci",
                                version="1.4.0", numpy="1.20.0", python="3.8", origin="conda-forge")


def test_count_metrics_of_single_session(monitor_service_v1):
    assert monitor_service_v1.count_metrics('b572200744a298a365bbbd1a8bb0cd21') == 13


def test_count_metrics_of_unknown_session(monitor_service_v1):
    assert monitor_service_v1.count_metrics('babc200744a298a365bbbd1a8bb0cd21') == 0


def test_count_metrics_of_single_context(monitor_service_v1):
    assert monitor_service_v1.count_metrics(context_h='28dae49c83587322a3b535612add39e3') == 130


def test_list_components(monitor_service_v1):
    components = monitor_service_v1.list_components()
    assert ['math.analytics', 'math.distance', 'math.prime'] == components


def test_list_sessions(monitor_service_v1):
    sessions = monitor_service_v1.list_sessions()
    assert len(sessions) == 20

    sessions = monitor_service_v1.list_sessions(with_tags=['version', 'numpy'],
                                                restrict_flags=["1.1.0", "1.18.5"],
                                                method="match_all")
    assert len(sessions) == 3
    for session in sessions.values():
        assert session.tags['version'] == "1.1.0"
        assert session.tags['numpy'] == "1.18.5"


def test_get_metrics(monitor_service_v1):
    metrics = monitor_service_v1.list_metrics()
    assert len(metrics) == 6


def test_metrics_with_context(monitor_service_v1):
    metrics = monitor_service_v1.list_context_metrics('9ae6c23d7c6b4562393385edf6da8500')
    assert len(metrics) == 6

    for metric in metrics:
        assert metric.context == '9ae6c23d7c6b4562393385edf6da8500'


def test_metrics_with_scm_ref(monitor_service_v1):
    metrics = monitor_service_v1.list_metrics_by_scm_id('4c3b3ca9e975a0a5eacd5d802d03c4ba690e8e41')
    assert len(metrics) == 4

    for metric in metrics:
        assert metric.session in ["b83742056ad0ed304d821562b7c209ff", "862004c16da83e7e2ce247a6c373d847",
                                  "085ec6cb63b2edf7a459b5c3fe62ffae", "47821a4727a078c94848b889e891317e"]


def test_metrics_by_type(monitor_service_v1):
    metrics = monitor_service_v1.list_metrics_by_type(MetricScope.FUNCTION)
    assert len(metrics) == 4

    for metric in metrics:
        assert metric.scope.name.lower() == 'function'

    metrics = monitor_service_v1.list_metrics_by_type(MetricScope.MODULE)
    assert len(metrics) == 2

    for metric in metrics:
        assert metric.scope.name.lower() == 'module'

    assert not monitor_service_v1.list_metrics_by_type(MetricScope.PACKAGE)


def test_metrics_by_pattern(monitor_service_v1):
    metrics = monitor_service_v1.list_metrics_from_pattern(variant='test_prime[1')
    assert len(metrics) == 2
    for metric in metrics:
        assert metric.variant.startswith('test_prime[1')

    metrics = monitor_service_v1.list_metrics_from_pattern(variant='not a variant')
    assert not metrics

    metrics = monitor_service_v1.list_metrics_from_pattern(item='test_p')
    assert len(metrics) == 2
    for metric in metrics:
        assert metric.item.startswith('test_p')

    metrics = monitor_service_v1.list_metrics_from_pattern(item='not a test')
    assert not metrics

    metrics = monitor_service_v1.list_metrics_from_pattern()
    assert metrics is not None
    assert not len(metrics)


def test_metrics_by_session(monitor_service_v1):
    metrics = monitor_service_v1.list_session_metrics('c9dd28cd8bb77f420a00dd229cc87f53')
    assert len(metrics) == 6

    for metric in metrics:
        assert metric.session == 'c9dd28cd8bb77f420a00dd229cc87f53'


def test_components(monitor_service_v1):
    assert monitor_service_v1.list_components() == ['math.analytics', 'math.distance', 'math.prime']


def test_contexts(monitor_service_v1):
    contexts = monitor_service_v1.list_contexts()
    assert len(contexts) == 2

    for h in ['9ae6c23d7c6b4562393385edf6da8500', '28dae49c83587322a3b535612add39e3']:
        assert h in contexts


def test_list_pipelines(monitor_service_v1):
    pipelines = monitor_service_v1.list_pipelines()
    assert len(pipelines) == 2
    assert sorted(pipelines) == ["master-py36", "master-py38"]


def test_list_pipeline_builds(monitor_service_v1):
    builds = monitor_service_v1.list_pipeline_builds("master-py36")
    assert len(builds) == 10
    assert [int(i) for i in builds] == [i for i in range(1, 11)]


def list_component_metrics(monitor_service_v1):
    m = monitor_service_v1.list_component_metrics('math.prime')
    assert len(m) == 4
    for metric in m:
        assert metric.component == 'math.prime'


def test_list_component_pipelines(monitor_service_v1):
    pipelines = monitor_service_v1.list_component_pipelines('math.prime')
    assert len(pipelines) == 2
    assert sorted(pipelines) == ["master-py36", "master-py38"]


def test_list_component_pipelines_build(monitor_service_v1):
    builds = monitor_service_v1.list_component_pipeline_builds('math.prime', "master-py36")
    assert len(builds) == 10
    assert [int(i) for i in builds] == [i for i in range(1, 11)]


def test__metrics_from(monitor_service_v1):
    pass


def test_get_component_metrics(monitor_service_v1):
    m = monitor_service_v1.list_component_metrics('math.prime')
    assert len(m) == 4
    for metric in m:
        assert metric.component == 'math.prime'


def test_get_item_metrics(monitor_service_v1):
    metrics = monitor_service_v1.list_item_metrics('test_prime')
    assert len(metrics) == 5
    variants = collections.Counter((metric.variant for metric in metrics))
    for metric in metrics:
        assert metric.item == 'test_prime'
    for variant in variants:
        assert variants[variant] == 1


def test_get_metrics_of_variant(monitor_service_v1):
    m = monitor_service_v1.list_metrics_of_variant('test_prime[2]')
    assert len(m) == 4
    for metric in m:
        assert metric.item == 'test_prime'
        assert metric.component in ['math.prime', 'math.prime2']
        assert metric.variant == 'test_prime[2]'

    m = monitor_service_v1.list_metrics_of_variant('test_prime[2]', 'math.prime')
    assert len(m) == 4
    for metric in m:
        assert metric.item == 'test_prime'
        assert metric.component == 'math.prime'
        assert metric.variant == 'test_prime[2]'

    m = monitor_service_v1.list_metrics_of_variant('test_prime[2]', 'math.distance')
    assert not len(m)


def test_context_details(monitor_service_v1):
    c = monitor_service_v1.get_context('28dae49c83587322a3b535612add39e3')
    assert c.h == '28dae49c83587322a3b535612add39e3'
    assert c.cpu_count == 8
    assert c.cpu_freq == 2500
    assert c.cpu_type == "i386"
    assert c.cpu_vendor == "Intel(R) Core(TM) i7-4870HQ CPU @ 2.50GHz"
    assert c.total_ram == 16384
    assert c.machine_node == "Rotondu.local"
    assert c.machine_type == "x86_64"
    assert c.machine_arch == "64bit"
    assert c.sys_info == "Darwin - 18.7.0"
    assert c.python_info == "3.8.6 | packaged by conda-forge | (default, Jan 25 2021, 23:22:12) [Clang 11.0.1 ]"

    assert monitor_service_v1.get_context('donotexist') is None


def test_get_metrics_from_resources(monitor_service_v1):
    metrics = monitor_service_v1.list_metrics_resources(ResourceType.MEMORY, ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.memory_usage)) for metric in metrics]
    exp = [('test_prime[982451653]', 10000), ('test_prime[982451653]', 9000),
           ('test_prime[982451653]', 8000), ('test_prime[982451653]', 7000),
           ('test_not_prime[524029229]', 6000)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources(ResourceType.MEMORY, ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.memory_usage)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 1000),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 2000),
           ('test_levenshtein', 3000), ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 4000),
           ('test_prime[2]', 5000)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources(ResourceType.CPU, ResourceMethod.TOP, 5)
    exp = [('test_prime[982451653]', 9), ('test_prime[982451653]', 8),
           ('test_prime[982451653]', 7), ('test_prime[982451653]', 6), ('test_not_prime[524029229]', 5)]

    got = [(metric.variant, int(metric.cpu_usage * 10)) for metric in metrics]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources(ResourceType.CPU, ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.cpu_usage * 100)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 10),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 20),
           ('test_levenshtein', 30), ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 40),
           ('test_prime[2]', 50)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources(ResourceType.KERNEL_TIME, ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.kernel_time * 100)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 10),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 20),
           ('test_levenshtein', 30), ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 40),
           ('test_prime[2]', 50)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources(ResourceType.KERNEL_TIME, ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.kernel_time * 100)) for metric in metrics]
    exp = [('test_prime[982451653]', 80), ('test_prime[982451653]', 70), ('test_prime[982451653]', 60),
           ('test_prime[982451653]', 50), ('test_not_prime[524029229]', 40)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources(ResourceType.USER_TIME, ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.user_time * 10)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 1),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 2), ('test_levenshtein', 3),
           ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 4), ('test_prime[2]', 5)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources(ResourceType.USER_TIME, ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.user_time * 10)) for metric in metrics]
    exp = [('test_prime[982451653]', 9), ('test_prime[982451653]', 8), ('test_prime[982451653]', 7),
           ('test_prime[982451653]', 6), ('test_not_prime[524029229]', 5)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources(ResourceType.TOTAL_TIME, ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.wall_time * 10)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 1),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 2), ('test_levenshtein', 3),
           ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 4), ('test_prime[2]', 5)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources(ResourceType.TOTAL_TIME, ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.wall_time * 10)) for metric in metrics]
    exp = [('test_prime[982451653]', 9), ('test_prime[982451653]', 8), ('test_prime[982451653]', 7),
           ('test_prime[982451653]', 6), ('test_not_prime[524029229]', 5)]
    assert got == exp


def test_get_metrics_resource_from_component(monitor_service_v1):
    component = 'math.prime'
    metrics = monitor_service_v1.list_metrics_resources_from_component(component, ResourceType.MEMORY,
                                                                       ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.memory_usage)) for metric in metrics]
    exp = [('test_prime[982451653]', 10000), ('test_prime[982451653]', 9000),
           ('test_prime[982451653]', 8000), ('test_prime[982451653]', 7000),
           ('test_not_prime[524029229]', 6000)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_component(component, ResourceType.MEMORY,
                                                                       ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.memory_usage)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 1000),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 2000),
           ('test_levenshtein', 3000), ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 4000),
           ('test_prime[2]', 5000)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_component(component, ResourceType.CPU,
                                                                       ResourceMethod.TOP, 5)
    exp = [('test_prime[982451653]', 9), ('test_prime[982451653]', 8),
           ('test_prime[982451653]', 7), ('test_prime[982451653]', 6), ('test_not_prime[524029229]', 5)]

    got = [(metric.variant, int(metric.cpu_usage * 10)) for metric in metrics]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_component(component, ResourceType.CPU,
                                                                       ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.cpu_usage * 100)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 10),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 20),
           ('test_levenshtein', 30), ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 40),
           ('test_prime[2]', 50)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_component(component, ResourceType.KERNEL_TIME,
                                                                       ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.kernel_time * 100)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 10),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 20),
           ('test_levenshtein', 30), ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 40),
           ('test_prime[2]', 50)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_component(component, ResourceType.KERNEL_TIME,
                                                                       ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.kernel_time * 100)) for metric in metrics]
    exp = [('test_prime[982451653]', 80), ('test_prime[982451653]', 70), ('test_prime[982451653]', 60),
           ('test_prime[982451653]', 50), ('test_not_prime[524029229]', 40)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_component(component, ResourceType.USER_TIME,
                                                                       ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.user_time * 10)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 1),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 2), ('test_levenshtein', 3),
           ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 4), ('test_prime[2]', 5)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_component(component, ResourceType.USER_TIME,
                                                                       ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.user_time * 10)) for metric in metrics]
    exp = [('test_prime[982451653]', 9), ('test_prime[982451653]', 8), ('test_prime[982451653]', 7),
           ('test_prime[982451653]', 6), ('test_not_prime[524029229]', 5)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_component(component, ResourceType.TOTAL_TIME,
                                                                       ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.wall_time * 10)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 1),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 2), ('test_levenshtein', 3),
           ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 4), ('test_prime[2]', 5)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_component(component, ResourceType.TOTAL_TIME,
                                                                       ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.wall_time * 10)) for metric in metrics]
    exp = [('test_prime[982451653]', 9), ('test_prime[982451653]', 8), ('test_prime[982451653]', 7),
           ('test_prime[982451653]', 6), ('test_not_prime[524029229]', 5)]
    assert got == exp


def test_get_metrics_resource_from_pipeline(monitor_service_v1):
    pipeline = 'master-py38'
    metrics = monitor_service_v1.list_metrics_resources_from_pipeline(pipeline, ResourceType.MEMORY,
                                                                      ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.memory_usage)) for metric in metrics]
    exp = [('test_prime[982451653]', 10000), ('test_prime[982451653]', 9000),
           ('test_prime[982451653]', 8000), ('test_prime[982451653]', 7000),
           ('test_not_prime[524029229]', 6000)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_pipeline(pipeline, ResourceType.MEMORY,
                                                                      ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.memory_usage)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 1000),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 2000),
           ('test_levenshtein', 3000), ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 4000),
           ('test_prime[2]', 5000)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_pipeline(pipeline, ResourceType.CPU,
                                                                      ResourceMethod.TOP, 5)
    exp = [('test_prime[982451653]', 9), ('test_prime[982451653]', 8),
           ('test_prime[982451653]', 7), ('test_prime[982451653]', 6), ('test_not_prime[524029229]', 5)]

    got = [(metric.variant, int(metric.cpu_usage * 10)) for metric in metrics]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_pipeline(pipeline, ResourceType.CPU,
                                                                      ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.cpu_usage * 100)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 10),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 20),
           ('test_levenshtein', 30), ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 40),
           ('test_prime[2]', 50)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_pipeline(pipeline, ResourceType.KERNEL_TIME,
                                                                      ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.kernel_time * 100)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 10),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 20),
           ('test_levenshtein', 30), ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 40),
           ('test_prime[2]', 50)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_pipeline(pipeline, ResourceType.KERNEL_TIME,
                                                                      ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.kernel_time * 100)) for metric in metrics]
    exp = [('test_prime[982451653]', 80), ('test_prime[982451653]', 70), ('test_prime[982451653]', 60),
           ('test_prime[982451653]', 50), ('test_not_prime[524029229]', 40)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_pipeline(pipeline, ResourceType.USER_TIME,
                                                                      ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.user_time * 10)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 1),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 2), ('test_levenshtein', 3),
           ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 4), ('test_prime[2]', 5)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_pipeline(pipeline, ResourceType.USER_TIME,
                                                                      ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.user_time * 10)) for metric in metrics]
    exp = [('test_prime[982451653]', 9), ('test_prime[982451653]', 8), ('test_prime[982451653]', 7),
           ('test_prime[982451653]', 6), ('test_not_prime[524029229]', 5)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_pipeline(pipeline, ResourceType.TOTAL_TIME,
                                                                      ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.wall_time * 10)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 1),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 2), ('test_levenshtein', 3),
           ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 4), ('test_prime[2]', 5)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_pipeline(pipeline, ResourceType.TOTAL_TIME,
                                                                      ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.wall_time * 10)) for metric in metrics]
    exp = [('test_prime[982451653]', 9), ('test_prime[982451653]', 8), ('test_prime[982451653]', 7),
           ('test_prime[982451653]', 6), ('test_not_prime[524029229]', 5)]
    assert got == exp


def test_get_metrics_resource_from_build(monitor_service_v1):
    pipeline = 'master-py38'
    build = "4"
    metrics = monitor_service_v1.list_metrics_resources_from_build(pipeline, build, ResourceType.MEMORY,
                                                                   ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.memory_usage)) for metric in metrics]
    exp = [('test_prime[982451653]', 10000), ('test_prime[982451653]', 9000),
           ('test_prime[982451653]', 8000), ('test_prime[982451653]', 7000),
           ('test_not_prime[524029229]', 6000)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_build(pipeline, build, ResourceType.MEMORY,
                                                                   ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.memory_usage)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 1000),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 2000),
           ('test_levenshtein', 3000), ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 4000),
           ('test_prime[2]', 5000)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_build(pipeline, build, ResourceType.CPU,
                                                                   ResourceMethod.TOP, 5)
    exp = [('test_prime[982451653]', 9), ('test_prime[982451653]', 8),
           ('test_prime[982451653]', 7), ('test_prime[982451653]', 6), ('test_not_prime[524029229]', 5)]

    got = [(metric.variant, int(metric.cpu_usage * 10)) for metric in metrics]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_build(pipeline, build, ResourceType.CPU,
                                                                   ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.cpu_usage * 100)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 10),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 20),
           ('test_levenshtein', 30), ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 40),
           ('test_prime[2]', 50)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_build(pipeline, build, ResourceType.KERNEL_TIME,
                                                                   ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.kernel_time * 100)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 10),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 20),
           ('test_levenshtein', 30), ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 40),
           ('test_prime[2]', 50)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_build(pipeline, build, ResourceType.KERNEL_TIME,
                                                                   ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.kernel_time * 100)) for metric in metrics]
    exp = [('test_prime[982451653]', 80), ('test_prime[982451653]', 70), ('test_prime[982451653]', 60),
           ('test_prime[982451653]', 50), ('test_not_prime[524029229]', 40)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_build(pipeline, build, ResourceType.USER_TIME,
                                                                   ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.user_time * 10)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 1),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 2), ('test_levenshtein', 3),
           ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 4), ('test_prime[2]', 5)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_build(pipeline, build, ResourceType.USER_TIME,
                                                                   ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.user_time * 10)) for metric in metrics]
    exp = [('test_prime[982451653]', 9), ('test_prime[982451653]', 8), ('test_prime[982451653]', 7),
           ('test_prime[982451653]', 6), ('test_not_prime[524029229]', 5)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_build(pipeline, build, ResourceType.TOTAL_TIME,
                                                                   ResourceMethod.LOWEST, 5)
    got = [(metric.variant, int(metric.wall_time * 10)) for metric in metrics]
    exp = [('test_compute_covariance_matrix[data_set0, expected_matrix0]', 1),
           ('test_compute_covariance_matrix[data_set1, expected_matrix1]', 2), ('test_levenshtein', 3),
           ('test_compute_covariance_matrix[data_set0, expected_matrix0]', 4), ('test_prime[2]', 5)]
    assert got == exp

    metrics = monitor_service_v1.list_metrics_resources_from_build(pipeline, build, ResourceType.TOTAL_TIME,
                                                                   ResourceMethod.TOP, 5)
    got = [(metric.variant, int(metric.wall_time * 10)) for metric in metrics]
    exp = [('test_prime[982451653]', 9), ('test_prime[982451653]', 8), ('test_prime[982451653]', 7),
           ('test_prime[982451653]', 6), ('test_not_prime[524029229]', 5)]
    assert got == exp


def test_get_metrics_from_sessions(monitor_service_v1):
    sessions = Sessions()
    session = sessions.add(monitor_service_v1.get_session('b83742056ad0ed304d821562b7c209ff'))
    metrics_from_session = monitor_service_v1.list_metrics_from(sessions=sessions)
    for metric in metrics_from_session:
        assert metric.session == session.h
    all_metrics = monitor_service_v1.list_metrics()
    metric_from_session_count = sum(1 for metric in all_metrics if metric.session == session.h)
    assert metric_from_session_count == len(metrics_from_session)


def test_get_metrics_from_contexts(monitor_service_v1):
    contexts = Contexts()
    context = contexts.add(monitor_service_v1.get_context('9ae6c23d7c6b4562393385edf6da8500'))
    metrics_from_context = monitor_service_v1.list_metrics_from(contexts=contexts)
    for metric in metrics_from_context:
        assert metric.context == context.h
    all_metrics = monitor_service_v1.list_metrics()
    metric_from_context_count = sum(1 for metric in all_metrics if metric.context == context.h)
    assert metric_from_context_count == len(metrics_from_context)


def test_get_metrics_from_sessions_contexts(monitor_service_v1):
    # We voluntary get a session linked to the context
    sessions, contexts = Sessions(), Contexts()
    session = sessions.add(monitor_service_v1.get_session('7768124332f353446557878a89ef6f4c'))
    context = contexts.add(monitor_service_v1.get_context('28dae49c83587322a3b535612add39e3'))

    metrics_from = monitor_service_v1.list_metrics_from(sessions=sessions, contexts=contexts)
    for metric in metrics_from:
        assert metric.context == context.h or metric.session == session.h
    all_metrics = monitor_service_v1.list_metrics()
    valid_metric_count = sum(1 for m in all_metrics if m.context == context.h or m.session == session.h)
    assert valid_metric_count == len(metrics_from.unique())


def test_get_sessions_from_metrics(monitor_service_v1):
    metrics = monitor_service_v1.list_metrics()
    sessions = monitor_service_v1.list_sessions_from(metrics)
    assert len(sessions) == 2
    for session in sessions.values():
        assert session.h in ['7768124332f353446557878a89ef6f4c', 'c4f6fe98a878755644353f2334218677']


def test_get_contexts_from_metrics(monitor_service_v1):
    metrics = monitor_service_v1.list_metrics()
    contexts = monitor_service_v1.list_contexts_from(metrics)
    assert len(contexts) == 2
    for context in contexts.values():
        assert context.h in ['7768124332f353446557878a89ef6f4c', 'c4f6fe98a878755644353f2334218677']


def test_get_sessions_from_build(monitor_service_v1):
    sessions = monitor_service_v1.list_build_sessions('master-py36', '4')
    assert len(sessions) == 2
    for session in sessions.values():
        assert session.tags['pipeline_branch'] == 'master-py36'
        assert session.tags['pipeline_build_no'] == '4'
