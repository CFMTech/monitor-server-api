# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from flask_restx import fields
from monitor_server import SERVER


def make_pageable(model):
    pageable = dict(model)
    pageable.update({'prev_url': fields.String(required=False,
                                               description='Url to previous page'),
                     'next_url': fields.String(required=False,
                                               description='Url to next page'),
                     'total_page': fields.Integer(required=False, default=1,
                                                  description='Total number of pages')})
    return pageable


# ------------------------------------------------------------------------------------------
#  Global namespaces
# ------------------------------------------------------------------------------------------
components_ns = SERVER.API_V1.namespace('components',
                                        description='Component based search and collections.')
filters_ns = SERVER.API_V1.namespace('filters', validate=True,
                                     description='Reads metrics from special filters.')
items_ns = SERVER.API_V1.namespace('items', validate=True,
                                   description='Item based search and collections of metrics.')
metrics_ns = SERVER.API_V1.namespace('metrics', validate=True,
                                     description='Access all metrics.')
pipelines_ns = SERVER.API_V1.namespace('pipelines',
                                       description='Address your metrics from your CI builds.')
resources_ns = SERVER.API_V1.namespace('resources',
                                       description='Find resource usage by items and variants.')
sessions_ns = SERVER.API_V1.namespace('sessions',
                                      description='Session based search and collection.')
variants_ns = SERVER.API_V1.namespace('variants', validate=True,
                                      description='Variants based search and collections of metrics.')
xcontexts_ns = SERVER.API_V1.namespace('contexts', description='Execution contexts based search and collection.')

# ------------------------------------------------------------------------------------------
#  Global schema
# ------------------------------------------------------------------------------------------
COMPONENT_LIST_SCHEMA = {
    'components': fields.List(fields.String(description="A component name"),
                              required=True, description="Full components list")
}

COMPONENT_PIPELINES_SCHEMA = {
    'component': fields.String(description="A component name", required=True),
    'pipelines': fields.List(fields.String(description="A pipeline identifier"),
                             required=True, description="List of pipelines for the given component.")
}

COMPONENT_PIPELINE_BUILDS_SCHEMA = {
    'component': fields.String(description="A component name", required=True),
    'pipeline': fields.String(description="A pipeline identifier", required=True),
    'builds': fields.List(fields.String(description='A build identifier.'),
                          required=True, description='List of builds for the given component on the given pipeline.')
}

COMPONENT_PIPELINE_BUILD_SESSIONS_SCHEMA = {
    'component': fields.String(description="A component name", required=True),
    'pipeline': fields.String(description="A pipeline identifier", required=True),
    'build': fields.String(description='A build identifier.', required=True),
    'sessions': fields.List(fields.String('A session identifier.'),
                            required=True,
                            description='List of all sessions associated to the given build, component and pipeline.')
}

EXEC_CONTEXT_FIELD_SCHEMA = {
    'h': fields.String(required=True, description="Unique Context identifier"),
    'cpu_count': fields.Integer(required=True, description='Number of available CPU'),
    'cpu_frequency': fields.Integer(required=True, attribute='cpu_freq',
                                    description='Nominal frequency of a CPU (in MHz)'),
    'cpu_type': fields.String(required=True, description='Architecture of the CPU'),
    'cpu_vendor': fields.String(required=False,
                                description='Information about constructor.'),
    'ram_total': fields.Integer(required=True,
                                description='Total RAM available'),
    'machine_node': fields.String(required=True, attribute='mac_node',
                                  description="Fully Qualified Domain Name (FQDN) of the machine  used for testing"),
    'machine_type': fields.String(required=True, attribute='mac_type',
                                  description="Machine architecture"),
    'machine_arch': fields.String(required=True, attribute='mac_arch',
                                  description="Bitmode of the machine"),
    'system_info': fields.String(required=True, attribute='sys_info',
                                 description="Short string about the Operating System"),
    'python_info': fields.String(required=True, attribute='py_info',
                                 description="Python information")
}


METRIC_FIELD_SCHEMA = {
    'session_h': fields.String(required=True, description='Session id on which the test has been run.'),
    'context_h': fields.String(required=True, attribute='ctx_h',
                               description='ExecutionContext id on which the test has been run.'),
    'item_start_time': fields.String(required=True, description='Effective start time of the test. Format: iso8601.'),
    'item_path': fields.String(required=True, description='Path of the item using Python import specification.'),
    'item': fields.String(required=True, description='Fully qualified name of the test (path/function_name)'),
    'item_variant': fields.String(required=True, description='Parametrization of the item.'),
    'item_fs_loc': fields.String(required=True,
                                 description="Relative path from pytest invocation directory to the item's module."),
    'kind': fields.String(required=True, description='Item type (class, function, module...)'),
    'component': fields.String(required=True, description='Component to which the test belong'),
    'total_time': fields.Float(required=True, attribute='wall_time',
                               description='Total time spent running the test (in seconds)'),
    'user_time':  fields.Float(required=True, description='Total time spent running in user space (in seconds)'),
    'kernel_time': fields.Float(required=True, attribute='krnl_time',
                                description='Total time spent running in kernel mode (in seconds)'),
    'cpu_usage': fields.Float(required=True, description='Percentage of CPU used while the test ran.'),
    'mem_usage': fields.Float(required=True, description='Memory used while running the test (in MB)')
}


TAG_FIELD_SCHEMA = {
    "name": fields.String(required=True, description='Tag name'),
    "value": fields.String(required=True, description="The tag's value")
}

PIPELINE_BUILDS_SCHEMA = {
    "pipeline": fields.String(required=True, description="CI Pipeline associated with following builds id."),
    "builds": fields.List(fields.String(required=True, description='Single build identifier'),
                          required=True, description='All available builds id for the given pipeline.')
}

PIPELINE_BUILD_SESSIONS_SCHEMA = {
    "pipeline": fields.String(required=True, description="CI Pipeline associated with following builds id."),
    "build": fields.String(required=True, description="Build identifier who has issued the following sessions id."),
    "sessions": fields.List(fields.String(required=True, description='Single Session identifier'),
                            required=True, description='All available sessions id for given pipeline and build id.')
}

# ------------------------------------------------------------------------------------------
#  Specific schema, might have some very specific models instantiated
# ------------------------------------------------------------------------------------------
SINGLE_COMPONENT_SCHEMA = {
    'name': fields.String(required=True, description="Full component name")
}

COMPONENT_METRICS_FIELD_SCHEMA = {
    'metrics': fields.List(fields.Nested(components_ns.model('metrics', METRIC_FIELD_SCHEMA))),
    'component': fields.String(required=True, description="Full component name")
}

COMPONENT_COUNT_SCHEMA = {
    'count': fields.Integer(required=True, description='Number of components')
}


EXECUTION_CONTEXT_METRICS_FIELD_SCHEMA = {
    'metrics': fields.List(fields.Nested(xcontexts_ns.model('metrics', METRIC_FIELD_SCHEMA)))
}

EXECUTION_CONTEXT_COUNT_SCHEMA = {
    'count': fields.Integer(required=True, description="Number of known execution contexts.")
}

METRIC_COUNT_SCHEMA = {
    'count': fields.Integer(required=True, description='Total count of metrics stored.')
}

SESSION_METRICS_FIELD_SCHEMA = {
    'metrics': fields.List(fields.Nested(sessions_ns.model('metrics', METRIC_FIELD_SCHEMA)))
}

SESSION_COUNT_SCHEMA = {
    'count': fields.Integer(required=True, description='Total count of sessions stored.')
}

single_tag_model = sessions_ns.model('SingleTag', TAG_FIELD_SCHEMA)

SESSION_FIELD_SCHEMA = {
    'session_h': fields.String(required=True, attribute='h',
                               description='Session id on which the test has been run.'),
    'run_date': fields.DateTime(dt_format='iso8601', required=True,
                                description='Date and time when test session has started. Format: iso8601.'),
    'scm_ref': fields.String(required=False, description='Reference to the SCM if any.'),
    'tags': fields.List(fields.Nested(single_tag_model),
                        required=True, description='List of all tags attached to a session.')
}

filter_single_tag_model = filters_ns.model('SingleTag', TAG_FIELD_SCHEMA)

FILTER_SESSION_FIELD_SCHEMA = {
    'session_h': fields.String(required=True, attribute='h',
                               description='Session id on which the test has been run.'),
    'run_date': fields.DateTime(dt_format='iso8601', required=True,
                                description='Date and time when test session has started. Format: iso8601.'),
    'scm_ref': fields.String(required=False, description='Reference to the SCM if any.'),
    'tags': fields.List(fields.Nested(filter_single_tag_model),
                        required=True, description='List of all tags attached to a session.')
}

SINGLE_BUILD_SCHEMA = {
    'id': fields.String(required=True, description='Pipeline identifier'),
    'sessions': fields.List(fields.String(required=True, description='Session hash identifier'),
                            required=True, description='List of sessions ran by this pipeline')
}

BUILD_PIPELINE_SCHEMA = {
    'pipeline': fields.String(required=True, description='Pipeline name'),
    'builds': fields.List(fields.Nested(pipelines_ns.model('SessionsByBuild', SINGLE_BUILD_SCHEMA)),
                          required=True, description='Builds issued from this pipeline')
}

PIPELINE_LIST_SCHEMA = {
    'pipelines': fields.List(fields.String(required=True, description='A pipeline name'),
                             required=True, description='List of pipelines known by the system')
}

# ------------------------------------------------------------------------------------------
#  Final models
# ------------------------------------------------------------------------------------------
# Components
single_component_model = components_ns.model('Component', SINGLE_COMPONENT_SCHEMA)

metrics_by_component_model = components_ns.model('MetricsByComponent', make_pageable(COMPONENT_METRICS_FIELD_SCHEMA))

component_list_model = components_ns.model('ComponentsList', make_pageable(COMPONENT_LIST_SCHEMA))

component_count_model = components_ns.model('ComponentsCount', COMPONENT_COUNT_SCHEMA)

component_pipelines_model = components_ns.model('ComponentPipelines', make_pageable(COMPONENT_PIPELINES_SCHEMA))

component_pipeline_builds_model = components_ns.model('ComponentPipelineBuilds',
                                                      make_pageable(COMPONENT_PIPELINE_BUILDS_SCHEMA))

component_pipeline_build_sessions_model = components_ns.model('ComponentPipelineBuildSessions',
                                                              make_pageable(COMPONENT_PIPELINE_BUILD_SESSIONS_SCHEMA))

# Execution contexts
xcontext_model = xcontexts_ns.model('ExecutionContext', EXEC_CONTEXT_FIELD_SCHEMA)

xcontext_list_model = xcontexts_ns.model('ExecutionContextsList',
                                         make_pageable({'contexts': fields.List(fields.Nested(xcontext_model))})
                                         )

metrics_by_xcontext_model = xcontexts_ns.model('MetricsByExecutionContext',
                                               make_pageable(EXECUTION_CONTEXT_METRICS_FIELD_SCHEMA)
                                               )
metrics_by_xcontext_count_model = xcontexts_ns.model('MetricsCount', METRIC_COUNT_SCHEMA)

xcontext_count_model = xcontexts_ns.model('ExecutionContextsCount', EXECUTION_CONTEXT_COUNT_SCHEMA)

# Filters
filtr_metrics_count_model = filters_ns.model('MetricsCount', METRIC_COUNT_SCHEMA)

filtr_metric_model = filters_ns.model('Metric', METRIC_FIELD_SCHEMA)

filtr_metric_list_model = filters_ns.model('MetricsList',
                                           make_pageable(
                                               {'metrics': fields.List(fields.Nested(filtr_metric_model))}
                                           ))

filtr_session_model = filters_ns.model('Session', FILTER_SESSION_FIELD_SCHEMA)
filtr_session_list_model = filters_ns.model('SessionList',
                                            make_pageable(
                                                {'sessions': fields.List(fields.Nested(filtr_session_model))}
                                            ))

# Items
item_metrics_count_model = metrics_ns.model('MetricsCount', METRIC_COUNT_SCHEMA)

item_metric_model = metrics_ns.model('Metric', METRIC_FIELD_SCHEMA)

item_metric_list_model = metrics_ns.model('MetricsList',
                                          make_pageable({'metrics': fields.List(fields.Nested(item_metric_model))})
                                          )

# Metrics
metric_count_model = metrics_ns.model('MetricsCount', METRIC_COUNT_SCHEMA)

metric_model = metrics_ns.model('Metric', METRIC_FIELD_SCHEMA)

metric_list_model = metrics_ns.model('MetricsList',
                                     make_pageable({'metrics': fields.List(fields.Nested(metric_model))})
                                     )

# Sessions
session_model = sessions_ns.model('Session', SESSION_FIELD_SCHEMA)

session_list_model = sessions_ns.model('SessionsList',
                                       make_pageable({'sessions': fields.List(fields.Nested(session_model))})
                                       )

metrics_by_session_list_model = sessions_ns.model('MetricsBySession', make_pageable(SESSION_METRICS_FIELD_SCHEMA))

session_count_model = sessions_ns.model('SessionCount', SESSION_COUNT_SCHEMA)

metrics_by_session_count_model = sessions_ns.model('MetricsCount', METRIC_COUNT_SCHEMA)

# Pipelines & builds
pipeline_model = pipelines_ns.model('SessionsByPipeline', make_pageable(BUILD_PIPELINE_SCHEMA))

pipeline_list_model = pipelines_ns.model('PipelineList', PIPELINE_LIST_SCHEMA)

pipeline_builds_model = pipelines_ns.model('PipelineBuilds', make_pageable(PIPELINE_BUILDS_SCHEMA))

pipeline_build_sessions_model = pipelines_ns.model('PipelineBuildSessions',
                                                   make_pageable(PIPELINE_BUILD_SESSIONS_SCHEMA))

# Resources
resource_metric_model = resources_ns.model('Metrics', METRIC_FIELD_SCHEMA)
resource_metrics_list_mode = resources_ns.model('MetricsByResource',
                                                make_pageable({
                                                    "metrics": fields.List(fields.Nested(resource_metric_model))
                                                })
                                                )

# Variants
vart_metrics_count_model = metrics_ns.model('MetricsCount', METRIC_COUNT_SCHEMA)

vart_metric_model = metrics_ns.model('Metric', METRIC_FIELD_SCHEMA)

vart_metric_list_model = metrics_ns.model('MetricsList',
                                          make_pageable({'metrics': fields.List(fields.Nested(vart_metric_model))})
                                          )
