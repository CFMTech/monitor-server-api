# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from flask_restx import Resource

from sqlalchemy import func

from http import HTTPStatus
from monitor_server import SERVER
from monitor_server.api.model import (resources_ns as ns, resource_metrics_list_mode)
from monitor_server.data.model import MetricModel, SessionModel


J_PIPELINE = '$.pipeline_branch'
J_BUILD = '$.pipeline_build_no'
RESOURCE_2_ENTITY = dict(memory=MetricModel.mem_usage, cpu=MetricModel.cpu_usage,
                         kernel_time=MetricModel.krnl_time, user_time=MetricModel.user_time,
                         total_time=MetricModel.wall_time)


@ns.route('/<string:resource>/head/metrics',
          defaults=dict(max_element=10),
          doc=dict(description='List up to 10 metrics from tests which consumes '
                               'most the given <resource>.'))
@ns.route('/<string:resource>/head/<int:max_element>/metrics',
          doc=dict(description='List up to <max_element> metrics from tests which consumes '
                               'most the given <resource>.'))
class ListHeadResource(Resource):
    @ns.marshal_list_with(resource_metrics_list_mode)
    @ns.response(int(HTTPStatus.OK), 'Success', resource_metrics_list_mode)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (No content)', resource_metrics_list_mode)
    def get(self, resource, max_element):
        max_element = min(max_element, 500)
        query = MetricModel.query.order_by(RESOURCE_2_ENTITY[resource].desc()).limit(max_element)
        items = [item for item in query]
        return dict(metrics=items)


@ns.route('/<string:resource>/tail/metrics',
          defaults=dict(max_element=10),
          doc=dict(description='List up to 10 metrics from tests which consumes '
                               'least the given <resource>.'))
@ns.route('/<string:resource>/tail/<int:max_element>/metrics',
          doc=dict(description='List up to <max_element> metrics from tests which consumes '
                               'least the given <resource>.'))
class ListTailResource(Resource):
    @ns.marshal_list_with(resource_metrics_list_mode)
    @ns.response(int(HTTPStatus.OK), 'Success', resource_metrics_list_mode)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (No content)', resource_metrics_list_mode)
    def get(self, resource, max_element):
        max_element = min(max_element, 500)
        query = MetricModel.query.order_by(RESOURCE_2_ENTITY[resource]).limit(max_element)
        items = [item for item in query]
        return dict(metrics=items)


# By pipeline
@ns.route('/<string:resource>/pipelines/<string:pipeline>/head/metrics',
          defaults=dict(max_element=10),
          doc=dict(description='List up to 10 metrics from tests which consumes'
                               'most the given <resource> on <pipeline>.'))
@ns.route('/<string:resource>/pipelines/<string:pipeline>/head/<int:max_element>/metrics',
          doc=dict(description='List up to <max_element> metrics from tests which consumes'
                               'most the given <resource> on <pipeline>.'))
class ListHeadResourceOfPipeline(Resource):
    @ns.marshal_list_with(resource_metrics_list_mode)
    @ns.response(int(HTTPStatus.OK), 'Success', resource_metrics_list_mode)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (No content)', resource_metrics_list_mode)
    def get(self, resource, pipeline, max_element):
        max_element = min(max_element, 500)
        session = SERVER.DB.session
        query = session.query(MetricModel)
        query = query.filter(func.json_extract(SessionModel.description, J_PIPELINE) == pipeline,
                             MetricModel.session_h == SessionModel.h)
        query = query.order_by(RESOURCE_2_ENTITY[resource].desc()).limit(max_element)
        items = [item for item in query]
        return dict(metrics=items)


@ns.route('/<string:resource>/pipelines/<string:pipeline>/tail/metrics',
          defaults=dict(max_element=10),
          doc=dict(description='List up to 10 metrics from tests which consumes'
                               'least the given <resource> on <pipeline>.'))
@ns.route('/<string:resource>/pipelines/<string:pipeline>/tail/<int:max_element>/metrics',
          doc=dict(description='List up to <max_element> metrics from tests which consumes'
                               'least the given <resource> on <pipeline>.'))
class ListTailResourceOfPipeline(Resource):
    @ns.marshal_list_with(resource_metrics_list_mode)
    @ns.response(int(HTTPStatus.OK), 'Success', resource_metrics_list_mode)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (No content)', resource_metrics_list_mode)
    def get(self, resource, pipeline, max_element):
        max_element = min(max_element, 500)
        session = SERVER.DB.session
        query = session.query(MetricModel)
        query = query.filter(func.json_extract(SessionModel.description, J_PIPELINE) == pipeline,
                             MetricModel.session_h == SessionModel.h)
        query = query.order_by(RESOURCE_2_ENTITY[resource]).limit(max_element)
        items = [item for item in query]
        return dict(metrics=items)


# By build
@ns.route('/<string:resource>/pipelines/<string:pipeline>/builds/<string:build>/head/metrics',
          defaults=dict(max_element=10),
          doc=dict(description='List up to 10 metrics from tests which consumes'
                               'most the given <resource> on (<pipeline>, <build>).'))
@ns.route('/<string:resource>/pipelines/<string:pipeline>/builds/<string:build>/head/<int:max_element>/metrics',
          doc=dict(description='List up to <max_element> metrics from tests which consumes'
                               'most the given <resource> on (<pipeline>, <build>).'))
class ListHeadResourceOfBuild(Resource):
    @ns.marshal_list_with(resource_metrics_list_mode)
    @ns.response(int(HTTPStatus.OK), 'Success', resource_metrics_list_mode)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (No content)', resource_metrics_list_mode)
    def get(self, resource, pipeline, build, max_element):
        max_element = min(max_element, 500)
        session = SERVER.DB.session
        query = session.query(MetricModel)
        query = query.filter(func.json_extract(SessionModel.description, J_PIPELINE) == pipeline,
                             func.json_extract(SessionModel.description, J_BUILD) == build,
                             MetricModel.session_h == SessionModel.h)
        query = query.order_by(RESOURCE_2_ENTITY[resource].desc()).limit(max_element)
        items = [item for item in query]
        return dict(metrics=items)


@ns.route('/<string:resource>/pipelines/<string:pipeline>/builds/<string:build>/tail/metrics',
          defaults=dict(max_element=10),
          doc=dict(description='List up to 10 metrics from tests which consumes'
                               'least the given <resource> on (<pipeline>, <build>).'))
@ns.route('/<string:resource>/pipelines/<string:pipeline>/builds/<string:build>/tail/<int:max_element>/metrics',
          doc=dict(description='List up to <max_element> metrics from tests which consumes'
                               'least the given <resource> on (<pipeline>, <build>).'))
class ListTailResourceOfBuild(Resource):
    @ns.marshal_list_with(resource_metrics_list_mode)
    @ns.response(int(HTTPStatus.OK), 'Success', resource_metrics_list_mode)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (No content)', resource_metrics_list_mode)
    def get(self, resource, pipeline, build, max_element):
        max_element = min(max_element, 500)
        session = SERVER.DB.session
        query = session.query(MetricModel)
        query = query.filter(func.json_extract(SessionModel.description, J_PIPELINE) == pipeline,
                             func.json_extract(SessionModel.description, J_BUILD) == build,
                             MetricModel.session_h == SessionModel.h)
        query = query.order_by(RESOURCE_2_ENTITY[resource]).limit(max_element)
        items = [item for item in query]
        return dict(metrics=items)


# By Component
@ns.route('/<string:resource>/components/<string:component>/head/metrics',
          defaults=dict(max_element=10),
          doc=dict(description='List up to 10 metrics from <component> which consumes '
                               'most the given <resource>.'))
@ns.route('/<string:resource>/components/<string:component>/head/<int:max_element>/metrics',
          doc=dict(description='List up to <max_element> metrics from <component> which consumes '
                               'most the given <resource>.'))
class ListHeadResourceOfComponent(Resource):
    @ns.marshal_list_with(resource_metrics_list_mode)
    @ns.response(int(HTTPStatus.OK), 'Success', resource_metrics_list_mode)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (No content)', resource_metrics_list_mode)
    def get(self, resource, component, max_element):
        max_element = min(max_element, 500)
        query = MetricModel.query.filter(MetricModel.component == component)
        query = query.order_by(RESOURCE_2_ENTITY[resource].desc()).limit(max_element)
        items = [item for item in query]
        return dict(metrics=items)


@ns.route('/<string:resource>/components/<string:component>/tail/metrics',
          defaults=dict(max_element=10),
          doc=dict(description='List up to 10 metrics from <component> which consumes '
                               'least the given <resource>.'))
@ns.route('/<string:resource>/components/<string:component>/tail/<int:max_element>/metrics',
          doc=dict(description='List up to <max_element> metrics from <component> which consumes '
                               'least the given <resource>.'))
class ListTailResourceOfComponent(Resource):
    @ns.marshal_list_with(resource_metrics_list_mode)
    @ns.response(int(HTTPStatus.OK), 'Success', resource_metrics_list_mode)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (No content)', resource_metrics_list_mode)
    def get(self, resource, component, max_element):
        max_element = min(max_element, 500)
        query = MetricModel.query.filter(MetricModel.component == component)
        query = query.order_by(RESOURCE_2_ENTITY[resource]).limit(max_element)
        items = [item for item in query]
        return dict(metrics=items)
