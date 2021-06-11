# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from flask import request
from flask_restx import Resource
from sqlalchemy import func

from http import HTTPStatus
from monitor_server import SERVER
from monitor_server.api.model import (xcontexts_ns as ns,
                                      xcontext_list_model, xcontext_model,
                                      xcontext_count_model, metrics_by_xcontext_model,
                                      metrics_by_xcontext_count_model)
from monitor_server.api.pager_utils import make_page
from monitor_server.data.model import ExecutionContextModel, MetricModel


@ns.route('/', defaults=dict(environ_hash=None),
          doc=dict(description='List all contexts with detailed information about them.'))
@ns.route('/<string:environ_hash>',
          doc=dict(description='List all contexts having their hash key starting with :environ_hash'
                               '. The listing is provided with detailed information.'))
class ListContexts(Resource):
    @ns.marshal_list_with(xcontext_list_model, skip_none=True)
    @ns.response(int(HTTPStatus.OK), 'Success', xcontext_list_model)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)', xcontext_list_model)
    def get(self, environ_hash):
        if environ_hash is None:
            query = ExecutionContextModel.query
        else:
            ctx_hash = f'{environ_hash}%'
            query = ExecutionContextModel.query.filter(ExecutionContextModel.h.like(ctx_hash))
        return make_page(request, query, 'contexts')

    @ns.marshal_with(xcontext_model)
    @ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation Error')
    @ns.response(int(HTTPStatus.CREATED), 'Success', xcontext_model)
    def post(self, environ_hash):
        value = ExecutionContextModel(h=request.json['h'],
                                      cpu_count=request.json['cpu_count'],
                                      cpu_freq=request.json['cpu_frequency'],
                                      cpu_type=request.json['cpu_type'],
                                      cpu_vendor=request.json['cpu_vendor'] if 'cpu_vendor' in request.json else '',
                                      ram_total=request.json['ram_total'],
                                      mac_node=request.json['machine_node'],
                                      mac_type=request.json['machine_type'],
                                      mac_arch=request.json['machine_arch'],
                                      sys_info=request.json['system_info'],
                                      py_info=request.json['python_info'])
        SERVER.DB.session.add(value)
        SERVER.DB.session.commit()
        return value, HTTPStatus.CREATED


@ns.route('/count', doc=dict(description='Count all contexts.'))
class CountContexts(Resource):
    @ns.marshal_list_with(xcontext_count_model)
    @ns.response(int(HTTPStatus.OK), 'Success', xcontext_count_model)
    def get(self):
        return dict(count=SERVER.DB.session.query(func.count(ExecutionContextModel.h)).first()[0])


@ns.route('/<string:context_hash>/metrics',
          doc=dict(description='Get all metrics linked to contexts with key :context_hash.'))
class ListMetricsByContext(Resource):
    @ns.marshal_list_with(metrics_by_xcontext_model, skip_none=True)
    @ns.response(int(HTTPStatus.OK), 'Success', metrics_by_xcontext_model)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)', metrics_by_xcontext_model)
    def get(self, context_hash):
        query = MetricModel.query.filter(MetricModel.ctx_h == context_hash)
        return make_page(request, query, 'metrics')


@ns.route('/<string:context_hash>/metrics/count',
          doc=dict(description='Count the total number of metrics linked to contexts with key :context_hash.'))
class CountMetricsByContext(Resource):
    @ns.marshal_list_with(metrics_by_xcontext_count_model)
    @ns.response(int(HTTPStatus.OK), 'Success', metrics_by_xcontext_count_model)
    def get(self, context_hash):
        db_session = SERVER.DB.session
        count = db_session.query(func.count(MetricModel.test_id))
        count = count.filter(MetricModel.ctx_h == context_hash)
        return dict(count=count.first()[0]), HTTPStatus.OK
