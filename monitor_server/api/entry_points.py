# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from flask import render_template
from monitor_server import __version__ as monitor_server_version
from monitor_server.api.components import (ListComponents, CountComponents, ListMetricsByComponent,
                                           ListComponentPipelines, ListComponentPipelineBuilds,
                                           ListSessionsOfComponentPipelineBuild,
                                           ListComponentMetricsByItem, ListComponentMetricsByVariant)
from monitor_server.api.execution_context import CountContexts, ListContexts
from monitor_server.api.metrics import (ListMetrics, CountMetrics,
                                        ListMetricsByItem, ListMetricsByItemPattern, CountMetricsByItem,
                                        ListMetricsByItemVariant, ListMetricsByItemVariantPattern,
                                        CountMetricsByItemVariant, ListSessionsByScm,
                                        ListMetricsByScm, CountMetricsBySCMRef,
                                        ListMetricsByType, CountMetricsByType)
from monitor_server.api.pipelines import ListPipelines, ListPipelineBuilds, ListSessionsOfBuildPipeline
from monitor_server.api.sessions import CountMetricsBySession, ListSessions, CountSessions, ListMetricsBySession
from monitor_server.api.resources import (ListHeadResource, ListTailResource,
                                          ListHeadResourceOfComponent, ListTailResourceOfComponent,
                                          ListHeadResourceOfPipeline, ListTailResourceOfPipeline,
                                          ListHeadResourceOfBuild, ListTailResourceOfBuild)
from monitor_server.data.model import MetricModel, SessionModel, ExecutionContextModel
from sqlalchemy import func


def _set_generic_entry_points(server):

    @server.route('/index.html')
    @server.route('/')
    def serve_index():
        session = server.DB.session
        metric_count = session.query(func.count(MetricModel.test_id)).first()[0]
        session_count = session.query(func.count(SessionModel.h)).first()[0]
        context_count = session.query(func.count(ExecutionContextModel.h)).first()[0]
        return render_template('index.html', metric_count=metric_count,
                               session_count=session_count, context_count=context_count,
                               version=monitor_server_version)


def _set_resource_access_entry_points(api):
    api.add_resource(CountComponents)
    api.add_resource(CountContexts)
    api.add_resource(CountMetricsByItem)
    api.add_resource(CountMetricsByItemVariant)
    api.add_resource(CountMetricsBySession)
    api.add_resource(CountMetrics)
    api.add_resource(CountMetricsBySCMRef)
    api.add_resource(CountMetricsByType)
    api.add_resource(CountSessions)
    api.add_resource(ListComponents)
    api.add_resource(ListComponentMetricsByItem)
    api.add_resource(ListComponentMetricsByVariant)
    api.add_resource(ListComponentPipelines)
    api.add_resource(ListComponentPipelineBuilds)
    api.add_resource(ListContexts)
    api.add_resource(ListSessionsByScm)
    api.add_resource(ListTailResource)
    api.add_resource(ListTailResourceOfBuild)
    api.add_resource(ListTailResourceOfComponent)
    api.add_resource(ListTailResourceOfPipeline)
    api.add_resource(ListMetrics)
    api.add_resource(ListMetricsByComponent)
    api.add_resource(ListMetricsByItem)
    api.add_resource(ListMetricsByItemPattern)
    api.add_resource(ListMetricsByItemVariant)
    api.add_resource(ListMetricsByItemVariantPattern)
    api.add_resource(ListMetricsByScm)
    api.add_resource(ListMetricsBySession)
    api.add_resource(ListMetricsByType)
    api.add_resource(ListPipelines)
    api.add_resource(ListPipelineBuilds)
    api.add_resource(ListHeadResource)
    api.add_resource(ListHeadResourceOfBuild)
    api.add_resource(ListHeadResourceOfComponent)
    api.add_resource(ListHeadResourceOfPipeline)
    api.add_resource(ListSessionsOfBuildPipeline)
    api.add_resource(ListSessionsOfComponentPipelineBuild)
    api.add_resource(ListSessions)


def set_entry_points(server):
    _set_generic_entry_points(server)
    _set_resource_access_entry_points(server.API_V1)
