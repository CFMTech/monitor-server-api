# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from flask import request
from flask_restx import Resource

from sqlalchemy import func

from http import HTTPStatus
from monitor_server import SERVER
from monitor_server.api.model import (pipelines_ns as ns, pipeline_list_model, pipeline_builds_model,
                                      pipeline_build_sessions_model)
from monitor_server.api.pager_utils import make_page
from monitor_server.data.model import SessionModel


J_PIPELINE = '$.pipeline_branch'
J_BUILD = '$.pipeline_build_no'


@ns.route('/', doc=dict(description='List all pipelines identifier.'))
class ListPipelines(Resource):
    @ns.marshal_list_with(pipeline_list_model)
    @ns.response(int(HTTPStatus.OK), 'Success', pipeline_list_model)
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (No content)', pipeline_list_model)
    def get(self):
        session = SERVER.DB.session
        pipelines = session.query(func.json_extract(SessionModel.description, J_PIPELINE)).\
            filter(func.json_extract(SessionModel.description, J_PIPELINE) != '').distinct()

        ppls = [pipeline[0] for pipeline in pipelines]
        if ppls:
            return dict(pipelines=ppls), HTTPStatus.OK
        return dict(), HTTPStatus.NO_CONTENT


@ns.route('/<string:pipeline>/builds', doc=dict(description='List all builds for pipeline :pipeline'))
class ListPipelineBuilds(Resource):
    @ns.marshal_with(pipeline_builds_model)
    @ns.response(int(HTTPStatus.OK), 'Success')
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (No content)')
    def get(self, pipeline):
        session = SERVER.DB.session
        ppl = session.query(func.json_extract(SessionModel.description, J_BUILD))
        ppl = ppl.filter(func.json_extract(SessionModel.description, J_PIPELINE) == pipeline,
                         func.json_extract(SessionModel.description, J_BUILD) != '')
        ppl = ppl.distinct()

        def collect(items):
            builds = []
            for item in items:
                builds.append(item[0])
            return dict(pipeline=pipeline, builds=builds)

        return make_page(request, ppl, None, collect)


@ns.route('/<string:pipeline>/builds/<string:build_no>/sessions',
          doc=dict(description='List all sessions for pipeline :pipeline and build :build_no'))
class ListSessionsOfBuildPipeline(Resource):
    @ns.marshal_with(pipeline_build_sessions_model)
    @ns.response(int(HTTPStatus.OK), 'Success')
    @ns.response(int(HTTPStatus.NO_CONTENT), 'Success (No content)')
    def get(self, pipeline, build_no):
        session = SERVER.DB.session
        ppl = session.query(SessionModel.h)
        ppl = ppl.filter(func.json_extract(SessionModel.description, J_PIPELINE) == pipeline,
                         func.json_extract(SessionModel.description, J_BUILD) == build_no)
        ppl = ppl.distinct()

        def collect(items):
            sessions = [item[0] for item in items]
            return dict(pipeline=pipeline, build=build_no, sessions=sessions)

        return make_page(request, ppl, None, collect)
