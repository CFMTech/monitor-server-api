# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from flask import request
from flask_restx import Resource

from sqlalchemy import func, distinct

from http import HTTPStatus
from monitor_server import SERVER
from monitor_server.api.model import (components_ns as ns, component_pipelines_model,
                                      component_pipeline_builds_model, component_pipeline_build_sessions_model,
                                      component_list_model, component_count_model, metrics_by_component_model)
from monitor_server.api.pager_utils import make_page
from monitor_server.data.model import MetricModel, SessionModel


@ns.route('/', defaults=dict(component=None),
          doc=dict(description='List all components.'))
@ns.route('/<string:component>',
          doc=dict(description='List all components having :component as prefix'))
class ListComponents(Resource):
    @ns.marshal_list_with(component_list_model, skip_none=True)
    @ns.response(int(HTTPStatus.OK), 'Success', component_list_model)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)', component_list_model)
    def get(self, component):
        all_components = SERVER.DB.session.query(MetricModel.component)
        if component is not None:
            pattern = f'{component}%'
            all_components = all_components.filter(MetricModel.component.like(pattern))
        all_components = all_components.distinct()
        return make_page(request, all_components, 'components', lambda x: [i[0] for i in x])


@ns.route('/count',
          doc=dict(description='Count total number of components (empty components are not taken into account.'))
class CountComponents(Resource):
    @ns.marshal_list_with(component_count_model)
    @ns.response(int(HTTPStatus.OK), 'Success', component_count_model)
    def get(self):
        count = SERVER.DB.session.query(func.count(distinct(MetricModel.component)))
        count = count.first()[0]
        return dict(count=max(count, count - 1)), HTTPStatus.OK


@ns.route('/<string:component>/metrics',
          doc=dict(description='List all metrics having belonging to component :component'))
@ns.route('/metrics', defaults=dict(component=None),
          doc=dict(description='List all metrics not belonging to a component (component is empty).'))
class ListMetricsByComponent(Resource):
    @ns.marshal_list_with(metrics_by_component_model, skip_none=True)
    @ns.response(int(HTTPStatus.OK), 'Success', metrics_by_component_model)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)')
    def get(self, component):
        if component is None:
            component = ''
        return make_page(request,
                         MetricModel.query.filter(MetricModel.component.like(component)),
                         'metrics')


@ns.route('/<string:component>/pipelines',
          doc=dict(description='List all pipelines which issued metrics for the component :component'))
class ListComponentPipelines(Resource):
    @ns.marshal_with(component_pipelines_model)
    @ns.response(int(HTTPStatus.OK), 'Success')
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)')
    def get(self, component):
        query = SERVER.DB.session.query
        query = query(func.json_extract(SessionModel.description, '$.pipeline_branch'))
        query = query.filter(MetricModel.component == component, MetricModel.session_h == SessionModel.h)
        query = query.distinct()

        def collect(items):
            return dict(component=component, pipelines=[item[0] for item in items])

        return make_page(request, query, collector=collect)


@ns.route('/<string:component>/pipelines/<string:pipeline>/builds',
          doc=dict(description='List all builds of pipeline :pipeline which issued metrics'
                               ' for the component :component'))
class ListComponentPipelineBuilds(Resource):
    @ns.marshal_with(component_pipeline_builds_model)
    @ns.response(int(HTTPStatus.OK), 'Success')
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)')
    def get(self, component, pipeline):
        query = SERVER.DB.session.query
        query = query(func.json_extract(SessionModel.description, '$.pipeline_build_no'))
        query = query.filter(MetricModel.component == component, MetricModel.session_h == SessionModel.h,
                             func.json_extract(SessionModel.description, '$.pipeline_branch') == pipeline,
                             func.json_extract(SessionModel.description, '$.pipeline_build_no') != ''
                             ).distinct()

        def collect(items):
            return dict(component=component, pipeline=pipeline, builds=[item[0] for item in items])

        return make_page(request, query, collector=collect)


@ns.route('/<string:component>/pipelines/<string:pipeline>/builds/<string:build_no>/sessions',
          doc=dict(description='List all sessions used by build :build_no on pipeline :pipeline'
                               ' for which metrics can be found with component :component.'))
class ListSessionsOfComponentPipelineBuild(Resource):
    @ns.marshal_with(component_pipeline_build_sessions_model)
    @ns.response(int(HTTPStatus.OK), 'Success')
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)')
    def get(self, component, pipeline, build_no):
        query = SERVER.DB.session.query
        comp_session_h = MetricModel.session_h.label('comp_session_h')
        inner_query = SERVER.DB.session.query(comp_session_h)
        inner_query = inner_query.filter(MetricModel.component == component).distinct().subquery()
        query = query(inner_query.c.comp_session_h)
        query = query.filter(func.json_extract(SessionModel.description, '$.pipeline_branch') == pipeline,
                             func.json_extract(SessionModel.description, '$.pipeline_build_no') == build_no,
                             inner_query.c.comp_session_h == SessionModel.h)
        query = query.distinct()

        def collect(items):
            return dict(component=component, pipeline=pipeline, build=build_no,
                        sessions=[item[0] for item in items])

        return make_page(request, query, collector=collect)


@ns.route('/<string:component>/items/<string:item>/metrics',
          doc=dict(description="List all metrics matching item for the specified component."))
@ns.route('/items/<string:item>/metrics', defaults=dict(component=None),
          doc=dict(description="List all metrics matching item without component set."))
class ListComponentMetricsByItem(Resource):
    @ns.marshal_list_with(metrics_by_component_model, skip_none=True)
    @ns.response(int(HTTPStatus.OK), 'Success', metrics_by_component_model)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)')
    def get(self, item, component):
        if component is None:
            component = ''
        session = SERVER.DB.session
        query = session.query(MetricModel).filter(MetricModel.component == component, MetricModel.item == item)
        return make_page(request, query, 'metrics')


@ns.route('/<string:component>/variants/<string:variant>/metrics',
          doc=dict(description="List all metrics matching variant for the specified component."))
@ns.route('/variants/<string:variant>/metrics', defaults=dict(component=None),
          doc=dict(description="List all metrics matching variant without component set."))
class ListComponentMetricsByVariant(Resource):
    @ns.marshal_list_with(metrics_by_component_model, skip_none=True)
    @ns.response(int(HTTPStatus.OK), 'Success', metrics_by_component_model)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)')
    def get(self, variant, component):
        if component is None:
            component = ''
        return make_page(request,
                         MetricModel.query.filter(MetricModel.component == component,
                                                  MetricModel.item_variant == variant),
                         'metrics')
