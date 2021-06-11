# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

import os
import pathlib

__version__ = '1.0.0'


def _create_monitor_server():
    if os.environ.get('MONITOR_SERVER_KEEP_PROXY', None) is None:
        for env in ['http_proxy', 'https_proxy']:  # pragma: no cover
            if env in os.environ:
                del os.environ[env]

    templates = pathlib.Path(__file__).parent / 'templates'
    server = Flask('monitor_server', template_folder=str(templates))

    mode = os.environ.get('FLASK_ENV', 'dev').lower()
    mode = 'dev' if mode not in ['prod', 'test'] else mode
    if mode == "prod" and "MONITOR_SERVER_DATABASE_URI" not in os.environ:  # pragma: no cover
        raise EnvironmentError('Missing path to database. Please configure it through '
                               'MONITOR_SERVER_DATABASE_URI environment variable')
    server.config.from_object(f'monitor_server.config.{mode.capitalize()}Config')
    v1 = Blueprint('v1', __name__, url_prefix='/api/v1')
    api = Api(v1, doc='/docs', validate=True, title='Monitor Server REST Api',
              description='REST Api to help you analyze data from pytest-monitor runs.',
              license='MIT LICENSE', license_url='https://opensource.org/licenses/MIT',
              contact='Jean-Sébastien Dieu', contact_email='jean-sebastien.dieu@cfm.fr')
    server.API_V1 = api
    server.register_blueprint(v1)
    db = SQLAlchemy(server)
    server.DB = db
    return server


SERVER = _create_monitor_server()
