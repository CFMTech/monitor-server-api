# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from flask import request
from flask_restx import Resource
from sqlalchemy import func, and_, or_

from http import HTTPStatus
from monitor_server import SERVER
from monitor_server.api.model import (sessions_ns as ns,
                                      session_count_model, session_list_model, metrics_by_session_count_model,
                                      metrics_by_session_list_model, session_model)
from monitor_server.api.pager_utils import make_page
from monitor_server.data.model import SessionModel, MetricModel


def _session_description_to_tag_listing(description):
    listing = [{'name': key, 'value': value} for key, value in description.items()]
    return listing


@ns.route('/', defaults=dict(session_hash=None),
          doc=dict(description='List all sessions.'))
@ns.route('/<string:session_hash>',
          doc=dict(description='List all sessions with key starting with :session_hash.'))
class ListSessions(Resource):
    @ns.marshal_list_with(session_list_model, skip_none=True)
    @ns.response(int(HTTPStatus.OK), 'Success', session_list_model)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)', session_list_model)
    def get(self, session_hash):

        def collect(items):
            d = []
            for session in items:
                a_session = dict(h=session.h, run_date=session.run_date,
                                 scm_ref=session.scm_ref,
                                 tags=_session_description_to_tag_listing(session.description))
                d.append(a_session)
            return d

        if session_hash is None:
            query = SessionModel.query
            collector = collect
        else:
            session_hash = f'{session_hash}%'
            query = SessionModel.query.filter(SessionModel.h.like(session_hash))
            collector = collect

        if request.args.get('with_flags', ''):
            method = request.args.get('method', 'match_any')
            with_flags = [f'$.{i}' for i in request.args.get('with_flags').split(',')]
            flags_restriction = request.args.get('restrict_flags', '').split(',')
            if len(flags_restriction) < len(with_flags):
                flags_restriction += [''] * (len(with_flags) - len(flags_restriction))
            cond = []
            for restrict_flag, restrict_value in zip(with_flags, flags_restriction):
                if restrict_value:
                    cond.append(func.json_extract(SessionModel.description, restrict_flag) == restrict_value)
                else:
                    cond.append(func.json_extract(SessionModel.description, restrict_flag) != '')
            else:
                if method == 'match_any':
                    query = query.filter(or_(*cond))
                else:
                    query = query.filter(and_(*cond))

        return make_page(request, query, 'sessions', collector=collector)

    @ns.marshal_list_with(session_model)
    @ns.response(int(HTTPStatus.CREATED), 'Success', session_model)
    @ns.response(int(HTTPStatus.BAD_REQUEST), 'Error')
    def post(self, session_hash):
        if type(request.json['description']) is not dict:
            return dict(message='Bad description format'), HTTPStatus.BAD_REQUEST
        session = SessionModel(h=request.json.get('session_h', session_hash),
                               run_date=request.json['run_date'],
                               scm_ref=request.json['scm_ref'],
                               description=request.json['description'])

        SERVER.DB.session.add(session)
        SERVER.DB.session.commit()
        return dict(h=session.h, run_date=session.run_date,
                    scm_ref=session.scm_ref,
                    tags=_session_description_to_tag_listing(session.description)), HTTPStatus.CREATED


@ns.route('/count',
          doc=dict(description='Count all sessions.'))
class CountSessions(Resource):
    @ns.marshal_list_with(session_count_model)
    @ns.response(int(HTTPStatus.OK), 'Success', session_count_model)
    def get(self):
        db_session = SERVER.DB.session
        count = db_session.query(func.count(SessionModel.scm_ref))
        return dict(count=count.first()[0]), HTTPStatus.OK


@ns.route('/<string:session_hash>/metrics',
          doc=dict(description='List all metric related to session :session_hash.'))
class ListMetricsBySession(Resource):
    @ns.marshal_list_with(metrics_by_session_list_model, skip_none=True)
    @ns.response(int(HTTPStatus.OK), 'Success', metrics_by_session_list_model)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (no content)', metrics_by_session_list_model)
    def get(self, session_hash):
        query = MetricModel.query.filter(MetricModel.session_h == session_hash)
        return make_page(request, query, 'metrics')


@ns.route('/<string:session_hash>/metrics/count',
          doc=dict(description='Count all metric related to session :session_hash'))
class CountMetricsBySession(Resource):
    @ns.marshal_list_with(metrics_by_session_count_model, skip_none=True)
    @ns.response(int(HTTPStatus.OK), 'Success', metrics_by_session_count_model)
    def get(self, session_hash):
        db_session = SERVER.DB.session
        count = db_session.query(func.count(MetricModel.test_id))
        count = count.filter(MetricModel.session_h == session_hash)
        return dict(count=count.first()[0]), HTTPStatus.OK


