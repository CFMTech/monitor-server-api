# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

import os


class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAGINATION_COUNT = int(os.environ.get('MONITOR_SERVER_PAGINATION_COUNT', 500))
    TESTING = False


class ProdConfig(Config):
    FLASK_ENV = 'production'
    SQLALCHEMY_ECHO = bool(int(os.environ.get('MONITOR_SERVER_ECHO_SQL', 0)))
    SQLALCHEMY_DATABASE_URI = os.environ.get("MONITOR_SERVER_DATABASE_URI")


class DevConfig(Config):
    DEBUG = True
    FLASK_ENV = 'dev'
    SQLALCHEMY_ECHO = bool(int(os.environ.get('MONITOR_SERVER_ECHO_SQL', 0)))
    SERVER_NAME = os.environ.get('SERVER', '127.0.0.1:5000')
    SQLALCHEMY_DATABASE_URI = os.environ.get("MONITOR_SERVER_DATABASE_URI", 'sqlite:////tmp/pymon')


class TestConfig(Config):
    ENV = 'test'
    TESTING = False
    SQLALCHEMY_ECHO = bool(int(os.environ.get('MONITOR_SERVER_ECHO_SQL', 0)))
    PAGINATION_COUNT = int(os.environ.get('MONITOR_SERVER_PAGINATION_COUNT', 5))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
