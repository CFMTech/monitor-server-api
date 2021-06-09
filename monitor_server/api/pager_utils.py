# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from flask import current_app, url_for
from http import HTTPStatus


PARAM_PAGE = 'page'
PARAM_ITEM_PER_PAGE = 'per_page'
DEFAULT_PAGINATION_COUNT = 500


def get_value_from_request(req, key, default, vtype=int):
    v = req.args.get(key, None, type=vtype)
    if v is None:
        if req.json is not None and key in req.json:
            return req.json[key]
        return default
    return v


def get_page_info(req):
    item_per_page = current_app.config.get('PAGINATION_COUNT', DEFAULT_PAGINATION_COUNT)
    page = get_value_from_request(req, PARAM_PAGE, 1)
    return page, item_per_page


def add_page_info(pagination, url, data, **url_params):
    if pagination.has_prev:
        params = dict(url_params['url_params']) if url_params.get('url_params', None) else dict()
        params.update({f'{PARAM_PAGE}': pagination.prev_num})
        prev_url = url_for(url, **params)
        data.update(dict(prev_url=prev_url))
    if pagination.has_next:
        params = dict(url_params['url_params']) if url_params.get('url_params', None) else dict()
        params.update({f'{PARAM_PAGE}': pagination.next_num})
        next_url = url_for(url, **params)
        data.update(dict(next_url=next_url))
    data.update(dict(total_page=pagination.pages))
    return data


def make_page(request, query, item_envelope=None, collector=None):
    page, count = get_page_info(request)
    if page < 0:
        pager = query.paginate(page=1, per_page=count)
        pager = query.paginate(page=pager.pages + page + 1, per_page=count)
    else:
        pager = query.paginate(page=page, per_page=count)
    if collector is None:
        content = [i for i in pager.items]
    else:
        content = collector(pager.items)
    if item_envelope is not None:
        data = {item_envelope: content}
    else:
        data = content
    args = dict()
    if request.view_args:
        args.update(request.view_args)
    if request.args:
        args.update(request.args)
    d = add_page_info(pager, request.endpoint, data, url_params=args)
    rc = HTTPStatus.OK if len(content) else HTTPStatus.NO_CONTENT
    return d, rc
