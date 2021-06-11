# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from flask import request
from flask_restx import Resource
from sqlalchemy import func

from http import HTTPStatus
from monitor_server import SERVER
from monitor_server.api.model import (metrics_ns, items_ns, variants_ns, filters_ns,
                                      metric_model, metric_list_model, metric_count_model,
                                      item_metric_list_model, item_metrics_count_model,
                                      vart_metric_list_model, vart_metrics_count_model,
                                      filtr_metric_list_model, filtr_metrics_count_model,
                                      filtr_session_list_model)
from monitor_server.api.pager_utils import make_page
from monitor_server.data.model import MetricModel, SessionModel


@metrics_ns.route('/',
                  doc=dict(description='List all metrics with detailed information.'))
class ListMetrics(Resource):
    @metrics_ns.marshal_list_with(metric_list_model, skip_none=True)
    @metrics_ns.response(int(HTTPStatus.OK), 'Success', metric_list_model)
    @metrics_ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)', metric_list_model)
    def get(self):
        return make_page(request, MetricModel.query, 'metrics')

    @metrics_ns.expect(metric_model)
    @metrics_ns.marshal_list_with(metric_model)
    @metrics_ns.response(int(HTTPStatus.CREATED), 'Success', metric_model)
    def post(self):
        metric = MetricModel(session_h=request.json['session_h'],
                             ctx_h=request.json['context_h'],
                             item_start_time=request.json['item_start_time'],
                             item_path=request.json['item_path'],
                             item=request.json['item'],
                             item_variant=request.json['item_variant'],
                             item_fs_loc=request.json['item_fs_loc'],
                             kind=request.json['kind'],
                             component=request.json['component'],
                             wall_time=request.json['total_time'],
                             user_time=request.json['user_time'],
                             krnl_time=request.json['kernel_time'],
                             cpu_usage=request.json['cpu_usage'],
                             mem_usage=request.json['mem_usage'])

        SERVER.DB.session.add(metric)
        SERVER.DB.session.commit()
        return metric, HTTPStatus.CREATED


@metrics_ns.route('/count', doc=dict(description='Count all metrics.'))
class CountMetrics(Resource):
    @metrics_ns.marshal_list_with(metric_count_model)
    @metrics_ns.response(int(HTTPStatus.OK), 'Success', metric_count_model)
    def get(self):
        db_session = SERVER.DB.session
        count = db_session.query(func.count(MetricModel.test_id))
        return dict(count=count.first()[0]), HTTPStatus.OK


@items_ns.route('/<string:item>/metrics',
                doc=dict(description='Get all metrics for test item :item. Listing contains all information'))
class ListMetricsByItem(Resource):
    @items_ns.marshal_list_with(item_metric_list_model, skip_none=True)
    @items_ns.response(int(HTTPStatus.OK), 'Success', item_metric_list_model)
    @items_ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)', item_metric_list_model)
    def get(self, item):
        return make_page(request, MetricModel.query.filter(MetricModel.item == item), 'metrics')


@items_ns.route('/<string:item>/metrics/count',
                doc=dict(description='Count all metrics for the given item.'))
class CountMetricsByItem(Resource):
    @items_ns.marshal_list_with(item_metrics_count_model, skip_none=True)
    @items_ns.response(int(HTTPStatus.OK), 'Success', item_metrics_count_model)
    def get(self, item):
        db_session = SERVER.DB.session
        query = db_session.query(func.count(MetricModel.test_id))
        query = query.filter(MetricModel.item == item)
        return dict(count=query.first()[0]), HTTPStatus.OK


@items_ns.route('/like/<string:item>/metrics',
                doc=dict(description='List all metrics having test item like :item'))
class ListMetricsByItemPattern(Resource):
    @items_ns.marshal_list_with(item_metric_list_model, skip_none=True)
    @items_ns.response(int(HTTPStatus.OK), 'Success', item_metric_list_model)
    @items_ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)', item_metric_list_model)
    def get(self, item):
        item = f'%{item}%'
        return make_page(request, MetricModel.query.filter(MetricModel.item.like(item)), 'metrics')


@variants_ns.route('/<string:variant>/metrics',
                   doc=dict(description='List all metric having for test variant :variant. '))
class ListMetricsByItemVariant(Resource):
    @variants_ns.marshal_list_with(vart_metric_list_model, skip_none=True)
    @variants_ns.response(int(HTTPStatus.OK), 'Success', vart_metric_list_model)
    @variants_ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)', vart_metric_list_model)
    def get(self, variant):
        return make_page(request, MetricModel.query.filter(MetricModel.item_variant == variant), 'metrics')


@variants_ns.route('/like/<string:variant>/metrics',
                   doc=dict(description='List all metrics having test variant like :variant'))
class ListMetricsByItemVariantPattern(Resource):
    @variants_ns.marshal_list_with(vart_metric_list_model, skip_none=True)
    @variants_ns.response(int(HTTPStatus.OK), 'Success', vart_metric_list_model)
    @variants_ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)', vart_metric_list_model)
    def get(self, variant):
        variant = f'%{variant}%'
        return make_page(request, MetricModel.query.filter(MetricModel.item_variant.like(variant)), 'metrics')


@variants_ns.route('/<string:variant>/metrics/count',
                   doc=dict(description='Count all metrics with the specified variant.'))
class CountMetricsByItemVariant(Resource):
    @variants_ns.marshal_list_with(vart_metrics_count_model, skip_none=True)
    @variants_ns.response(int(HTTPStatus.OK), 'Success', vart_metrics_count_model)
    def get(self, variant):
        db_session = SERVER.DB.session
        query = db_session.query(func.count(MetricModel.test_id))
        query = query.filter(MetricModel.item_variant == variant)
        return dict(count=query.first()[0]), HTTPStatus.OK


@filters_ns.route('/scope/<string:scope>/metrics',
                  doc=dict(description='List all metric with type set to :kind'))
class ListMetricsByType(Resource):
    @filters_ns.marshal_list_with(filtr_metric_list_model, skip_none=True)
    @filters_ns.response(int(HTTPStatus.OK), 'Success', filtr_metric_list_model)
    @filters_ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)', filtr_metric_list_model)
    def get(self, scope):
        return make_page(request, MetricModel.query.filter(MetricModel.kind == scope), 'metrics')


@filters_ns.route('/scope/<string:scope>/metrics/count',
                  doc=dict(description='Count all metric with type set to :kind'))
class CountMetricsByType(Resource):
    @filters_ns.marshal_list_with(filtr_metrics_count_model, skip_none=True)
    @filters_ns.response(int(HTTPStatus.OK), 'Success', filtr_metrics_count_model)
    def get(self, scope):
        query = SERVER.DB.session.query(func.count(MetricModel.test_id))
        query = query.filter(MetricModel.kind == scope)
        return dict(count=query.first()[0]), HTTPStatus.OK


@filters_ns.route('/scm/<string:scm>/metrics/count',
                  doc=dict(description='Count all metrics related to SCM reference :scm.'))
class CountMetricsBySCMRef(Resource):
    @filters_ns.marshal_list_with(filtr_metrics_count_model)
    @filters_ns.response(int(HTTPStatus.OK), 'Success', filtr_metrics_count_model)
    def get(self, scm=None):
        db_session = SERVER.DB.session
        scm = f'{scm}%'
        sessions = [s.h for s in SessionModel.query.filter(SessionModel.scm_ref.like(scm)).all()]
        if not sessions:
            return dict(count=0)
        count = db_session.query(func.count(MetricModel.test_id)).filter(MetricModel.session_h.in_(sessions))
        return dict(count=count.first()[0]), HTTPStatus.OK


@filters_ns.route('/scm/<string:scm_id>/metrics',
                  doc=dict(description='Get all metrics with sessions having their SCM reference set to :scm_id.'))
class ListMetricsByScm(Resource):
    @filters_ns.marshal_list_with(filtr_metric_list_model, skip_none=True)
    @filters_ns.response(int(HTTPStatus.OK), 'Success', filtr_metric_list_model)
    @filters_ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)', filtr_metric_list_model)
    def get(self, scm_id):
        scm = f'{scm_id}%'
        sessions = [s.h for s in SessionModel.query.filter(SessionModel.scm_ref.like(scm)).all()]
        if not sessions:
            return {'metrics': []}, HTTPStatus.NO_CONTENT
        return make_page(request, MetricModel.query.filter(MetricModel.session_h.in_(sessions)), 'metrics')


@filters_ns.route('/scm/<string:scm_id>/sessions',
                  doc=dict(description='Get all sessions with SCM reference set to :scm_id'))
class ListSessionsByScm(Resource):
    @filters_ns.marshal_list_with(filtr_session_list_model, skip_none=True)
    @filters_ns.response(int(HTTPStatus.OK), 'Success', filtr_session_list_model)
    @filters_ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)', filtr_session_list_model)
    def get(self, scm_id):
        scm = f'{scm_id}%'
        sessions = SessionModel.query.filter(SessionModel.scm_ref.like(scm))
        return make_page(request, sessions, 'sessions')
