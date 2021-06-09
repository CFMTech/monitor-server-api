# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from monitor_api.enums import MetricScope, ResourceType, ResourceMethod
from monitor_api.core.collections import Contexts, Metrics, Sessions
from monitor_api.core.entities import Context, Metric, Session
from monitor_api.dialects.dialect import Dialect
from http import HTTPStatus
from typing import Optional, List, Dict, Any, Union
import requests


def translate(context: Optional[Dict[str, Any]] = None,
              metric: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if context is not None:
        d = dict(h=context['h'],
                 cpu_count=context['cpu_count'],
                 cpu_freq=context['cpu_frequency'],
                 cpu_type=context['cpu_type'],
                 cpu_vendor=context['cpu_vendor'],
                 ram_total=context['ram_total'],
                 mac_node=context['machine_node'],
                 mac_type=context['machine_type'],
                 mac_arch=context['machine_arch'],
                 sys_info=context['system_info'],
                 py_info=context['python_info'])
    else:
        d = dict(context_h=metric['context_h'],
                 session_h=metric['session_h'],
                 start_time=metric['item_start_time'],
                 item_path=metric['item_path'],
                 item=metric['item'],
                 variant=metric['item_variant'],
                 path=metric['item_fs_loc'],
                 component=metric['component'],
                 wall_time=metric['total_time'],
                 user_time=metric['user_time'],
                 kernel_time=metric['kernel_time'],
                 cpu_usage=metric['cpu_usage'],
                 memory_usage=metric['mem_usage'])
        if metric['kind'].lower() == 'function':
            d.update(dict(kind=MetricScope.FUNCTION))
        elif metric['kind'].lower() == 'module':
            d.update(dict(kind=MetricScope.MODULE))
        else:
            d.update(dict(kind=MetricScope.PACKAGE))
    return d


class Remote(Dialect):
    def __init__(self, url, **kwargs):
        self.__session = requests.session()
        self.__url = url.rstrip('/')
        for i in ['headers', 'cookies', 'auth', 'proxies', 'hooks', 'params', 'verify',
                  'cert', 'adapters', 'stream', 'trust_env', 'max_redirects']:
            if i in kwargs:
                setattr(self.__session, i, kwargs[i])
        if 'adapter' in kwargs:
            self.__session.mount(self.__url, kwargs['adapter'])

    def _make_url(self, path, **params):
        url = f'{self.__url}/{path.lstrip("/")}'
        if not params:
            return url
        params = '&'.join([f'{k}={v}' for k, v in params.items()])
        return f'{url}?{params}'

    def _collect(self, url):
        r = self.__session.get(url)
        while True:
            if r.status_code == HTTPStatus.OK:
                yield r.json()
                r.status_code = HTTPStatus.NO_CONTENT
            else:
                break
            url = r.json().get('next_url', None)
            if url is not None:
                r = self.__session.get(f'{self._make_url(url)}')

    def count_sessions(self) -> int:
        try:
            j = self.__session.get(self._make_url('/sessions/count')).json()
            return j.get('count', -1)
        except requests.RequestException:
            return -1

    def count_components(self) -> int:
        try:
            j = self.__session.get(self._make_url('/components/count')).json()
            return j.get('count', -1)
        except requests.RequestException:
            return -1

    def count_contexts(self) -> int:
        try:
            j = self.__session.get(self._make_url('/contexts/count')).json()
            return j.get('count', -1)
        except requests.RequestException:
            return -1

    def count_metrics(self, session_h: str = None, context_h: str = None, scm_ref: str = None) -> int:
        try:
            if session_h:
                j = self.__session.get(self._make_url(f'/sessions/{session_h}/metrics/count')).json()
            elif context_h:
                j = self.__session.get(self._make_url(f'/contexts/{context_h}/metrics/count')).json()
            elif scm_ref:
                j = self.__session.get(self._make_url(f'/filters/scm/{scm_ref}/metrics/count')).json()
            else:
                j = self.__session.get(self._make_url('/metrics/count')).json()
            return j.get('count', -1)
        except requests.RequestException:
            return -1

    def get_session_details(self, session_h) -> Optional[Session]:
        try:
            j = self.__session.get(self._make_url(f'/sessions/{session_h}'))
            if j.status_code == HTTPStatus.NO_CONTENT:
                return None
            return Session(**j.json()['sessions'])
        except requests.RequestException:
            return None

    def get_components(self) -> List[str]:
        try:
            j = self.__session.get(self._make_url(f'/components/'))
            if j.status_code == HTTPStatus.NO_CONTENT:
                return []
            return j.json()['components']
        except requests.RequestException:
            return []

    def get_sessions(self, with_tags: Union[str, List[str]] = None,
                     restrict_flags: Union[str, List[str]] = None,
                     method: str = None) -> Sessions:
        sessions = Sessions()
        url = '/sessions/'
        params = dict()
        if with_tags:
            params['with_tags'] = ','.join(with_tags) if type(with_tags) is list else with_tags
        if restrict_flags:
            params['restrict_flags'] = ','.join(restrict_flags) if type(restrict_flags) is list else restrict_flags
        if params and method:
            params['method'] = method
        try:
            for page in self._collect(self._make_url(url, **params)):
                for session in page['sessions']:
                    s = Session(**session)
                    sessions[s.h] = s
            return sessions
        except requests.RequestException:
            return Sessions()

    def get_metrics(self) -> Metrics:
        metrics = Metrics()
        try:
            for page in self._collect(self._make_url('/metrics/')):
                for metric in page['metrics']:
                    metrics.append(Metric(**translate(metric=metric)))
            return metrics
        except requests.RequestException:
            return Metrics()

    def get_metrics_with_context(self, context_h: str) -> Metrics:
        metrics = Metrics()
        try:
            for page in self._collect(self._make_url(f'/contexts/{context_h}/metrics')):
                for metric in page['metrics']:
                    metrics.append(Metric(**translate(metric=metric)))
            return metrics
        except requests.RequestException:
            return Metrics()

    def get_metrics_with_scm_ref(self, scm_ref: str) -> Metrics:
        metrics = Metrics()
        try:
            for page in self._collect(self._make_url(f'/filters/scm/{scm_ref}/metrics')):
                for metric in page['metrics']:
                    metrics.append(Metric(**translate(metric=metric)))
            return metrics
        except requests.RequestException:
            return Metrics()

    def get_metrics_by_type(self, metric_type: MetricScope) -> Metrics:
        metrics = Metrics()
        try:
            for page in self._collect(self._make_url(f'/filters/scope/{metric_type.value}/metrics')):
                for metric in page['metrics']:
                    metrics.append(Metric(**translate(metric=metric)))
            return metrics
        except requests.RequestException:
            return Metrics()

    def get_metrics_by_pattern(self, item: str = None, variant: str = None) -> Metrics:
        if item is not None:
            base_url = f'/items/like/{item}/metrics'
        elif variant is not None:
            base_url = f'/variants/like/{variant}/metrics'
        else:
            return Metrics()
        m = Metrics()
        try:
            for page in self._collect(self._make_url(base_url)):
                for metric in page['metrics']:
                    m.append(Metric(**translate(metric=metric)))
            return m
        except requests.RequestException:
            return Metrics()

    def get_metrics_by_session(self, session_h: str) -> Metrics:
        m = Metrics()
        try:
            for page in self._collect(self._make_url(f'/sessions/{session_h}/metrics')):
                for metric in page['metrics']:
                    m.append(Metric(**translate(metric=metric)))
            return m
        except requests.RequestException:
            return Metrics()

    def get_contexts(self) -> Contexts:
        c = Contexts()
        try:
            for page in self._collect(self._make_url('/contexts/')):
                for context in page['contexts']:
                    ctx = Context(**translate(context=context))
                    c[ctx.h] = ctx
            return c
        except requests.RequestException:
            return Contexts()

    def get_pipelines(self) -> List[str]:
        try:
            data = self.__session.get(self._make_url('/pipelines/'))
            if data.status_code == HTTPStatus.NO_CONTENT:
                return []
            return [ppl for ppl in data.json()['pipelines']]
        except requests.RequestException:
            return []

    def get_pipeline_builds(self, pipeline: str) -> List[str]:
        try:
            blds = []
            for page in self._collect(self._make_url(f'/pipelines/{pipeline}/builds')):
                blds.extend((build for build in page['builds']))
            return blds
        except requests.RequestException:
            return []

    def read_component_metrics(self, component: Optional[str] = None) -> Metrics:
        m = Metrics()
        try:
            base_url = '/components/metrics' if component is None else f'/components/{component}/metrics'
            for page in self._collect(self._make_url(base_url)):
                for metric in page['metrics']:
                    m.append(Metric(**translate(metric=metric)))
            return m
        except requests.RequestException:
            return Metrics()

    def get_component_pipelines(self, component: str) -> List[str]:
        try:
            ppls = []
            for page in self._collect(self._make_url(f'/components/{component}/pipelines')):
                ppls.extend((ppl for ppl in page['pipelines']))
            return ppls
        except requests.RequestException:
            return []

    def get_component_pipelines_build(self, component: str, pipeline: str) -> List[str]:
        try:
            builds = []
            for page in self._collect(self._make_url(f'/components/{component}/pipelines/{pipeline}/builds')):
                builds.extend((bld for bld in page['builds']))
            return builds
        except requests.RequestException:
            return []

    def get_item_metrics(self, item: str) -> Metrics:
        m = Metrics()
        try:
            for page in self._collect(self._make_url(f'/items/{item}/metrics')):
                for metric in page['metrics']:
                    m.append(Metric(**translate(metric=metric)))
            return m
        except requests.RequestException:
            return Metrics()

    def get_metrics_of_variant(self, variant: str, component: str = None) -> Metrics:
        m = Metrics()
        url = f'/variants/{variant}/metrics'
        if component:
            url = f'/components/{component}/variants/{variant}/metrics'
        try:
            for page in self._collect(self._make_url(url)):
                for metric in page['metrics']:
                    m.append(Metric(**translate(metric=metric)))
            return m
        except requests.RequestException:
            return Metrics()

    def get_context_details(self, context_h: str) -> Optional[Context]:
        try:
            data = self.__session.get(self._make_url(f'/contexts/{context_h}'))
            if data.status_code == HTTPStatus.OK:
                return Context(**translate(context=data.json()))
            return None
        except requests.RequestException:
            return None

    def get_metrics_by_resource(self, resource: ResourceType, method: ResourceMethod = ResourceMethod.TOP,
                                max_element: int = 10) -> Metrics:
        which = {res.value: res.name.lower() for res in ResourceType}
        method = "head" if method == ResourceMethod.TOP else "tail"
        url = f'/resources/{which[resource.value]}/{method}/{max_element}/metrics'
        metrics = Metrics()
        try:
            for page in self._collect(self._make_url(url)):
                for metric in page["metrics"]:
                    metrics.append(Metric(**translate(metric=metric)))
            return metrics
        except requests.RequestException:
            return Metrics()

    def get_metrics_by_component_resource(self, resource: ResourceType, component: str,
                                          method: ResourceMethod = ResourceMethod.TOP,
                                          max_element: int = 10) -> Metrics:
        which = {res.value: res.name.lower() for res in ResourceType}
        method = "head" if method == ResourceMethod.TOP else "tail"
        url = f'/resources/{which[resource.value]}/components/{component}/{method}/{max_element}/metrics'
        metrics = Metrics()
        try:
            for page in self._collect(self._make_url(url)):
                for metric in page["metrics"]:
                    metrics.append(Metric(**translate(metric=metric)))
            return metrics
        except requests.RequestException:
            return Metrics()

    def get_metrics_by_pipeline_resource(self, resource: ResourceType, pipeline: str,
                                         method: ResourceMethod = ResourceMethod.TOP,
                                         max_element: int = 10) -> Metrics:
        which = {res.value: res.name.lower() for res in ResourceType}
        method = "head" if method == ResourceMethod.TOP else "tail"
        url = f'/resources/{which[resource.value]}/pipelines/{pipeline}/{method}/{max_element}/metrics'
        metrics = Metrics()
        try:
            for page in self._collect(self._make_url(url)):
                for metric in page["metrics"]:
                    metrics.append(Metric(**translate(metric=metric)))
            return metrics
        except requests.RequestException:
            return Metrics()

    def get_metrics_by_build_resource(self, resource: ResourceType, pipeline: str, build: str,
                                      method: ResourceMethod = ResourceMethod.TOP,
                                      max_element: int = 10) -> Metrics:
        which = {res.value: res.name.lower() for res in ResourceType}
        method = "head" if method == ResourceMethod.TOP else "tail"
        url = f'/resources/{which[resource.value]}/pipelines/{pipeline}/builds/{build}/{method}/{max_element}/metrics'
        metrics = Metrics()
        try:
            for page in self._collect(self._make_url(url)):
                for metric in page["metrics"]:
                    metrics.append(Metric(**translate(metric=metric)))
            return metrics
        except requests.RequestException:
            return Metrics()

    def get_metrics_from(self, sessions: Sessions = None, contexts: Contexts = None) -> Metrics:
        m = Metrics()
        if sessions:
            for h in set(sessions.keys()):
                ms = self.get_metrics_by_session(h)
                m = Metrics.merge(m, ms)
        if contexts:
            for h in set(contexts.keys()):
                ms = self.get_metrics_with_context(h)
                m = Metrics.merge(m, ms)
        return m

    def get_sessions_from(self, metrics: Metrics) -> Sessions:
        s = Sessions()
        for metric in metrics:
            if metric.session not in s:
                s[metric.session] = self.get_session_details(metric.session)
        return s

    def get_contexts_from(self, metrics: Metrics) -> Contexts:
        c = Contexts()
        for metric in metrics:
            if metric.context not in c:
                c[metric.context] = self.get_context_details(metric.context)
        return c

    def get_sessions_from_build(self, pipeline: str, build_id: str) -> Sessions:
        url = f'/pipelines/{pipeline}/builds/{build_id}/sessions'
        sessions = Sessions()
        try:
            for page in self._collect(self._make_url(url)):
                for session in page["sessions"]:
                    sessions.add(self.get_session_details(session))
            return sessions
        except requests.RequestException:
            return Sessions()
