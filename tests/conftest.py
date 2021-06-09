# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from http import HTTPStatus
import datetime
import json
import os
import pathlib
import pytest
import random
import requests
import re
import string
import sqlite3
import yaml


os.environ['FLASK_ENV'] = 'test'
os.environ["SQLALCHEMY_ECHO"] = "1"

from monitor_server import SERVER
from monitor_server.data.model import *
from monitor_server.api.entry_points import set_entry_points as set_api_entry_points
from monitor_api.monitor import Monitor as APIMonitor
import requests_mock as rm

DATADIR = pathlib.Path(__file__).parent / 'data'


@pytest.fixture(scope='session')
def monitor_db():
    data_path = pathlib.Path(__file__).parent / "data" / "data.yaml"
    datas = yaml.load(data_path.read_text(), Loader=yaml.FullLoader)
    model_path = pathlib.Path(__file__).parent / "data" / "db.json"
    model = json.loads(model_path.read_text())
    db_path = pathlib.Path(__file__).parent / 'pymonitor.db'
    if db_path.exists():
        db_path.unlink()
    c = sqlite3.connect(str(db_path))
    cursor = c.cursor()
    for table in model["db"]["tables"]:
        cursor.execute(f'{model["db"]["model"][table]["create"]};')
        insert_stmt = model["db"]["model"][table]["insert"]
        insert_keys = model["db"]["model"][table]["insert_keys"]
        for data in datas[f'{table}'].values():
            t = tuple((data[k] for k in insert_keys))
            c.execute(insert_stmt, t)
        c.commit()
    yield APIMonitor(str(db_path))
    db_path.unlink()


@pytest.fixture(scope='function')
def monitor_db_no_data():
    model_path = pathlib.Path(__file__).parent / "data" / "db.json"
    model = json.loads(model_path.read_text())
    db_path = pathlib.Path(__file__).parent / 'pymonitor.db'
    if db_path.exists():
        db_path.unlink()
    c = sqlite3.connect(str(db_path))
    cursor = c.cursor()
    for table in model["db"]["tables"]:
        cursor.execute(f'{model["db"]["model"][table]["create"]};')
        c.commit()
    yield APIMonitor(str(db_path))
    db_path.unlink()


@pytest.fixture(scope='function')
def monitor_service_v1(request):
    test = request.node.originalname or request.node.name
    try:
        data_path = pathlib.Path(__file__).parent / "data" / f"{test}.service.json"
        data = json.loads(data_path.read_text())
    except FileNotFoundError:
        data_path = pathlib.Path(__file__).parent / "data" / "service.json"
        data = json.loads(data_path.read_text())

    def cb(req, context):
        query_url = req.path
        if req.query:
            query_url += f'?{req.query}'
        context.status_code = data[query_url]['status_code']
        return data[query_url]['data']

    adapter = rm.Adapter()
    url = re.compile('https://monitor.service/api/v1/')
    adapter.register_uri('GET', url, json=cb)
    yield APIMonitor('https://monitor.service/api/v1/', adapter=adapter)


@pytest.fixture(scope='session')
def monitor_service_v1_no_data(request):
    # data_path = pathlib.Path(__file__).parent / "data" / "service.json"
    # data = json.loads(data_path.read_text())

    def cb(req, context):
        test = req.path
        context.status_code = HTTPStatus.NO_CONTENT
        if "count" in test:
            return dict(count=0)
        return dict()

    adapter = rm.Adapter()
    url = re.compile('https://monitor.service/api/v1/')
    adapter.register_uri('GET', url, json=cb)
    yield APIMonitor('https://monitor.service/api/v1/', adapter=adapter)


@pytest.fixture(scope='session')
def monitor_service_v1_not_up():

    def cb(request, context):
        raise requests.HTTPError("Unable to contact")

    adapter = rm.Adapter()
    url = re.compile('https://monitor.service/api/v1/')
    adapter.register_uri('GET', url, json=cb)
    yield APIMonitor('https://monitor.service/api/v1/', adapter=adapter)


class Monitor:
    def __init__(self, a_client):
        self.__c = a_client

    @property
    def client(self):
        return self.__c

    def assert_session_count(self, count):
        r = self.__c.get('/api/v1/sessions/count')
        assert r.status_code == HTTPStatus.OK
        assert r.json['count'] == count

    def assert_metric_count(self, count):
        r = self.__c.get('/api/v1/metrics/count')
        assert r.status_code == HTTPStatus.OK
        assert r.json['count'] == count

    def assert_context_count(self, count):
        r = self.__c.get('/api/v1/contexts/count')
        assert r.status_code == HTTPStatus.OK
        assert r.json['count'] == count

    def assert_no_components(self):
        assert self.__c.get('/api/v1/components/').status_code == HTTPStatus.NO_CONTENT

    def assert_no_sessions(self):
        assert self.__c.get('/api/v1/sessions/').status_code == HTTPStatus.NO_CONTENT

    def assert_no_contexts(self):
        assert self.__c.get('/api/v1/contexts/').status_code == HTTPStatus.NO_CONTENT

    def assert_no_metrics(self):
        assert self.__c.get('/api/v1/metrics/').status_code == HTTPStatus.NO_CONTENT

    def post_sessions_v1(self, *args):
        for s in args:
            assert self.__c.post('/api/v1/sessions/', json=s).status_code == HTTPStatus.CREATED

    def post_contexts_v1(self, *args):
        for c in args:
            assert self.__c.post('/api/v1/contexts/', json=c).status_code == HTTPStatus.CREATED

    def post_metrics_v1(self, *args):
        for m in args:
            assert self.__c.post('/api/v1/metrics/', json=m).status_code == HTTPStatus.CREATED


class Generator:
    def __init__(self):
        pass

    @staticmethod
    def random_float(low=0, high=100):
        return random.random() * (high - low) + low

    @staticmethod
    def random_floats(count, low=0, high=100):
        return [random.random() * (high - low) + low for _ in range(count)]

    @staticmethod
    def random_string(length=15, letters=None):
        letters = letters or string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def random_strings(count, length=15, letters=None):
        letters = letters or string.ascii_letters
        return [''.join(random.choice(letters) for _ in range(length)) for _ in range(count)]

    @staticmethod
    def random_pypath(compound=4):
        return '.'.join((Generator.random_string() for _ in range(compound)))

    @staticmethod
    def random_path(compound=4):
        return '/'.join((Generator.random_string() for _ in range(compound)))

    @staticmethod
    def random_pypaths(count, compound=4):
        return ['.'.join((Generator.random_string() for _ in range(compound))) for _ in range(count)]

    @staticmethod
    def random_paths(count, compound=4):
        return ['/'.join((Generator.random_string() for _ in range(compound))) for _ in range(count)]

    @staticmethod
    def new_metric(context, session, **fixed):
        item = Generator.random_string()
        return dict(session_h=session['session_h'],
                    context_h=context['h'],
                    item_start_time=fixed.get('item_start_time',
                                              datetime.datetime.utcnow().isoformat()),
                    item_path=fixed.get('item_path', Generator.random_pypath()),
                    item=fixed.get('item', item),
                    item_variant=fixed.get('item_variant', item),
                    kind=fixed.get('kind', 'function'),
                    item_fs_loc=fixed.get('item_fs_loc', Generator.random_path() + '.py'),
                    component=fixed.get('component', Generator.random_string(8)),
                    total_time=fixed.get('total_time', random.random() * 100),
                    user_time=fixed.get('user_time', random.random() * 50),
                    kernel_time=fixed.get('kernel_time', random.random() * 10),
                    cpu_usage=fixed.get('cpu_usage', random.random() * 30),
                    mem_usage=fixed.get('mem_usage', random.random() * 1000))

    @staticmethod
    def new_jenkins_session(pipeline='jenkinsci:monitor', buildno='1', **fixed):
        return Generator.new_session(pipeline_build_no=buildno, pipeline_branch=pipeline, __ci__='jenkinsci', **fixed)

    @staticmethod
    def new_circleci_session(pipeline='circleci:monitor', buildno='1', **fixed):
        return Generator.new_session(pipeline_build_no=buildno, pipeline_branch=pipeline, __ci__='circleci', **fixed)

    @staticmethod
    def new_droneci_session(pipeline='droneci:monitor', buildno='1', **fixed):
        return Generator.new_session(pipeline_build_no=buildno, pipeline_branch=pipeline, __ci__='droneci', **fixed)

    @staticmethod
    def new_travisci_session(pipeline='travisci:monitor', buildno='1', **fixed):
        return Generator.new_session(pipeline_build_no=buildno, pipeline_branch=pipeline, __ci__='travisci', **fixed)

    @staticmethod
    def new_gitlab_session(pipeline='gitlabci:monitor', buildno='1', **fixed):
        return Generator.new_session(pipeline_build_no=buildno, pipeline_branch=pipeline, __ci__='gitlabci', **fixed)

    @staticmethod
    def new_session(**fixed):
        if not fixed.get('force_description'):
            level = fixed.get('level', Generator.random_string(4, string.digits))
            py = fixed.get('python', f'py{Generator.random_string(2, string.digits)}')
            project = fixed.get('project', Generator.random_string(8))
            build_no = fixed.get('pipeline_build_no', Generator.random_string(3, string.digits))
            build_br = fixed.get('pipeline_branch', Generator.random_string(8))
            j = dict(level=level, python=py, project=project,
                     pipeline_branch=build_br, pipeline_build_no=build_no)
            j.update(fixed.get('description', dict()))
        else:
            j = fixed.get('force_description')
        return dict(session_h=fixed.get('session_h', Generator.random_string(32)),
                    run_date=fixed.get('run_date', datetime.datetime.utcnow().isoformat()),
                    scm_ref=fixed.get('scm_ref', Generator.random_string(48)),
                    description=j)

    @staticmethod
    def new_context(**fixed):
        return dict(h=fixed.get('h', Generator.random_string(32)),
                    cpu_count=fixed.get('cpu_count', random.randint(0, 100)),
                    cpu_frequency=fixed.get('cpu_frequency', random.randint(1500, 5000)),
                    cpu_type=fixed.get('cpu_type', 'x86_64'),
                    cpu_vendor=fixed.get('cpu_vendor', Generator.random_string(48)),
                    ram_total=fixed.get('ram_total', random.randint(100000, 1000000)),
                    machine_node=fixed.get('machine_node', f'{Generator.random_string(20)}.fr.cfm.fr'),
                    machine_type=fixed.get('machine_type', 'x86'),
                    machine_arch=fixed.get('machine_arch', '64 bits'),
                    system_info=fixed.get('system_info', Generator.random_string(48)),
                    python_info=fixed.get('python_info', Generator.random_string(48)))


@pytest.fixture(scope='session')
def app():
    with SERVER.app_context():
        set_api_entry_points(SERVER)
        SERVER.DB.create_all()
        yield SERVER
        SERVER.DB.session.remove()


@pytest.fixture(scope='function', autouse=True)
def session(app, request):
    """Creates a new database session for a test."""
    connection = app.DB.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = app.DB.create_scoped_session(options=options)

    app.DB.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture()
def monitor(client):
    return Monitor(client)


@pytest.fixture()
def gen():
    return Generator()
