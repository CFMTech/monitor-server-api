# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from http import HTTPStatus


def test_empty_components(client):
    resp = client.get('/api/v1/components/')
    assert resp.status_code == HTTPStatus.NO_CONTENT


def test_empty_execution_contexts(client):
    resp = client.get('/api/v1/contexts/')
    assert resp.status_code == HTTPStatus.NO_CONTENT


def test_empty_metrics(client):
    resp = client.get('/api/v1/metrics/')
    assert resp.status_code == HTTPStatus.NO_CONTENT


def test_empty_pipelines(client):
    resp = client.get('/api/v1/pipelines/')
    assert resp.status_code == HTTPStatus.NO_CONTENT


def test_empty_sessions(client):
    resp = client.get('/api/v1/sessions/')
    assert resp.status_code == HTTPStatus.NO_CONTENT


def test_empty_components_count(client):
    resp = client.get('/api/v1/components/count')
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == dict(count=0)


def test_empty_context_count(client):
    resp = client.get('/api/v1/contexts/count')
    assert resp.json == dict(count=0)
    assert resp.status_code == HTTPStatus.OK


def test_empty_metrics_count(client):
    resp = client.get('/api/v1/metrics/count')
    assert resp.json == dict(count=0)
    assert resp.status_code == HTTPStatus.OK


def test_empty_sessions_count(client):
    resp = client.get('/api/v1/sessions/count')
    assert resp.json == dict(count=0)
    assert resp.status_code == HTTPStatus.OK
