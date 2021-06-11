# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from monitor_api.enums import ResourceMethod, MetricScope, ResourceType
from monitor_api.dialects.dialect import Dialect
from monitor_api.core.collections import Contexts, Metrics, Sessions
from monitor_api.core.entities import Context, Metric, Session
import json
import sqlite3
from typing import List, Optional, Union


FIELD_TRANSLATION_DICT = dict(session=dict(session_h='h', run_date='run_date',
                                           scm_id='scm_ref', run_description='tags'),
                              context=dict(env_h='h', cpu_frequency_mhz='cpu_freq', ram_total_mb='ram_total',
                                           machine_node='mac_node', machine_type='mac_type',
                                           machine_arch='mac_arch', system_info='sys_info', python_info='py_info'),
                              metric=dict(h='session_h', env_h='context_h', item_start_time='start_time',
                                          item_variant='variant', item_fs_loc='path', total_time='wall_time',
                                          mem_usage='memory_usage'),
                              )


class Local(Dialect):
    def __init__(self, path: str, **kwargs):
        self.__translation_ctx = dict()

        def row_factory(cursor, row):
            d = dict()
            for idx, col in enumerate(cursor.description):
                k = col[0].lower()
                k = self.__translation_ctx.get(k, k)
                if k == 'tags':
                    try:
                        d[k] = json.loads(row[idx])
                    except json.JSONDecodeError:
                        d[k] = dict()
                elif k.startswith('count(distinct') or k.startswith('count'):
                    d['count'] = row[idx]
                elif k == 'kind':
                    if row[idx] == 'function':
                        d[k] = MetricScope.FUNCTION
                    elif row[idx] == 'module':
                        d[k] = MetricScope.MODULE
                    else:
                        d[k] = MetricScope.PACKAGE
                else:
                    d[k] = row[idx]
            return d

        self.__cnx = sqlite3.connect(str(path), **kwargs)
        self.__cnx.row_factory = row_factory

    def _set_tr_context(self, value: str):
        if not value:
            self.__translation_ctx = dict()
        else:
            self.__translation_ctx = FIELD_TRANSLATION_DICT.get(value, dict())

    def get_sessions(self, with_tags: Union[str, List[str]] = None,
                     restrict_flags: Union[str, List[str]] = None,
                     method: str = None) -> Sessions:
        sessions = Sessions()
        self._set_tr_context('session')
        conditions = ''
        binds = []
        if with_tags or restrict_flags:
            method = ' OR ' if method == 'match_any' else ' AND '
            tags = with_tags if type(with_tags) is list else with_tags.split(',')
            values = restrict_flags if type(restrict_flags) is list else restrict_flags.split(',')
            if len(values) < len(tags):
                values += [''] * (len(tags) - len(values))
            conds = []
            for restrict_flag, restrict_value in zip(tags, values):
                if restrict_value:
                    conds.append(f'json_extract(RUN_DESCRIPTION, "$.{restrict_flag}") = ?')
                    binds.append(restrict_value)
                else:
                    conds.append(f'json_extract(RUN_DESCRIPTION, "$.{restrict_flag}") != \'\'')
            conditions = method.join(conds)
        try:
            if conditions:
                conditions = f'WHERE {conditions}'
            query = f'select * from TEST_SESSIONS {conditions};'
            binds = tuple(binds)
            for row in self.__cnx.execute(query, binds).fetchall():
                s = Session(**row)
                sessions[s.h] = s
        except sqlite3.Error:
            return Sessions()
        return sessions

    def get_metrics(self) -> Metrics:
        metrics = Metrics()
        self._set_tr_context('metric')
        try:
            for row in self.__cnx.execute('select * from TEST_METRICS;').fetchall():
                # row['kind'] = dict(function=MetricType.FUNCTION,
                #                    module=MetricType.MODULE,
                #                    package=MetricType.PACKAGE)[row['kind']]
                metrics.append(Metric(**row))
        except sqlite3.Error:
            return Metrics()
        return metrics

    def get_metrics_with_context(self, context_h: str) -> Metrics:
        query = "SELECT * from TEST_METRICS WHERE ENV_H = ?"
        m = Metrics()
        self._set_tr_context('metric')
        try:
            for row in self.__cnx.execute(query, (context_h,)).fetchall():
                m.append(Metric(**row))
        except sqlite3.Error:
            return Metrics()
        return m

    def get_metrics_with_scm_ref(self, scm_ref: str) -> Metrics:
        query = "select SESSION_H from TEST_SESSIONS where SCM_ID = ?;"
        m = Metrics()
        self._set_tr_context('metric')
        try:
            sessions = [row['session_h'] for row in self.__cnx.execute(query, (scm_ref,)).fetchall()]
            for session_h in sessions:
                stmt = "SELECT * from TEST_METRICS WHERE SESSION_H = ?"
                for row in self.__cnx.execute(stmt, (session_h,)).fetchall():
                    m.append(Metric(**row))
            return m
        except sqlite3.Error:
            return Metrics()

    def get_metrics_by_type(self, metric_type: MetricScope) -> Metrics:
        if metric_type.value == MetricScope.FUNCTION.value:
            query = "SELECT * FROM TEST_METRICS WHERE KIND = 'function';"
        elif metric_type.value == MetricScope.MODULE.value:
            query = "SELECT * FROM TEST_METRICS WHERE KIND = 'module';"
        else:
            query = "SELECT * FROM TEST_METRICS WHERE KIND = 'package';"
        m = Metrics()
        self._set_tr_context('metric')
        try:
            for row in self.__cnx.execute(query).fetchall():
                m.append(Metric(**row))
            return m
        except sqlite3.Error:
            return Metrics()

    def get_metrics_by_pattern(self, item: str = None, variant: str = None) -> Metrics:
        if item is not None:
            query = "SELECT * FROM TEST_METRICS WHERE ITEM LIKE ?"
            bind = (f'{item}%',)
        elif variant is not None:
            query = "SELECT * FROM TEST_METRICS WHERE ITEM_VARIANT LIKE ?"
            bind = (f'{variant}%',)
        else:
            return Metrics()
        m = Metrics()
        try:
            self._set_tr_context('metric')
            for row in self.__cnx.execute(query, bind).fetchall():
                m.append(Metric(**row))
            return m
        except sqlite3.Error:
            return Metrics()

    def get_metrics_by_session(self, session_h: str) -> Metrics:
        query = 'SELECT * FROM TEST_METRICS WHERE SESSION_H = ?'
        m = Metrics()
        self._set_tr_context('metric')
        try:
            for row in self.__cnx.execute(query, (session_h,)).fetchall():
                m.append(Metric(**row))
            return m
        except sqlite3.Error:
            return Metrics()

    def get_components(self) -> List[str]:
        comps = []
        self._set_tr_context('')
        try:
            for row in self.__cnx.execute('select DISTINCT(COMPONENT) from TEST_METRICS;').fetchall():
                comps.append(row['component'])
        except sqlite3.Error:
            return []
        return comps

    def get_contexts(self) -> Contexts:
        contexts = Contexts()
        self._set_tr_context('context')
        try:
            for row in self.__cnx.execute('select * from EXECUTION_CONTEXTS;').fetchall():
                c = Context(**row)
                contexts[c.h] = c
        except sqlite3.Error:
            return Contexts()
        return contexts

    def count_components(self) -> int:
        query = "select COUNT(DISTINCT(COMPONENT)) from TEST_METRICS where COMPONENT != '';"
        try:
            row = self.__cnx.execute(query).fetchone()
            return int(row['count'])
        except sqlite3.Error:
            return -1

    def count_contexts(self) -> int:
        query = "select COUNT(DISTINCT(ENV_H)) from EXECUTION_CONTEXTS;"
        try:
            row = self.__cnx.execute(query).fetchone()
            return int(row['count'])
        except sqlite3.Error:
            return -1

    def _count_metrics_by_session(self, session_h: str) -> int:
        query = "select COUNT(*) from TEST_METRICS where SESSION_H = ?;"
        try:
            row = self.__cnx.execute(query, (session_h,)).fetchone()
            return int(row['count'])
        except sqlite3.Error:
            return -1

    def _count_all_metrics(self) -> int:
        query = "select COUNT(*) from TEST_METRICS;"
        try:
            row = self.__cnx.execute(query).fetchone()
            return int(row['count'])
        except sqlite3.Error:
            return -1

    def _count_metrics_by_context(self, context_h: str) -> int:
        query = "select COUNT(*) from TEST_METRICS where ENV_H = ?;"
        try:
            row = self.__cnx.execute(query, (context_h,)).fetchone()
            return int(row['count'])
        except sqlite3.Error:
            return -1

    def _count_metrics_by_scm_ref(self, scm_ref: str) -> int:
        query = "select SESSION_H from TEST_SESSIONS where SCM_ID = ?;"
        try:
            sessions = [row['session_h'] for row in self.__cnx.execute(query, (scm_ref,)).fetchall()]
            count = sum((self._count_metrics_by_session(session) for session in sessions))
            return count
        except sqlite3.Error:
            return -1

    def count_metrics(self, session_h: str = None, context_h: str = None, scm_ref: str = None) -> int:
        if session_h is None and scm_ref is None and context_h is None:
            return self._count_all_metrics()
        if session_h is not None:
            return self._count_metrics_by_session(session_h)
        elif context_h is not None:
            return self._count_metrics_by_context(context_h)
        else:
            return self._count_metrics_by_scm_ref(scm_ref)

    def count_sessions(self) -> int:
        query = "select COUNT(DISTINCT(SESSION_H)) from TEST_SESSIONS;"
        try:
            row = self.__cnx.execute(query).fetchone()
            return int(row['count'])
        except sqlite3.Error:
            return -1

    def get_session_details(self, session_h) -> Optional[Session]:
        try:
            self._set_tr_context('session')
            row = self.__cnx.execute('SELECT * FROM TEST_SESSIONS WHERE SESSION_H = ?', (session_h,)).fetchone()
            return Session(**row) if row is not None else None
        except sqlite3.Error:
            return None

    def get_pipelines(self) -> List[str]:
        query = "select distinct(json_extract(RUN_DESCRIPTION, '$.pipeline_branch')) as PIPELINES " \
                "from TEST_SESSIONS" \
                " where json_extract(RUN_DESCRIPTION, '$.pipeline_branch') != ''"
        try:
            row = self.__cnx.execute(query).fetchall()
            return [i['pipelines'] for i in row]
        except sqlite3.Error:
            return []

    def get_pipeline_builds(self, pipeline: str) -> List[str]:
        query = "select json_extract(RUN_DESCRIPTION, '$.pipeline_build_no') as BUILDS" \
                " from TEST_SESSIONS " \
                " where json_extract(RUN_DESCRIPTION, '$.pipeline_branch') = ?"
        try:
            row = self.__cnx.execute(query, (pipeline,)).fetchall()
            return [i['builds'] for i in row]
        except sqlite3.Error:
            return []

    def read_component_metrics(self, component: Optional[str] = None) -> Metrics:
        query = "select * from TEST_METRICS where COMPONENT = ?"
        bind = (component,) if component is not None else ('', )
        m = Metrics()
        self._set_tr_context('metric')
        try:
            for row in self.__cnx.execute(query, bind).fetchall():
                m.append(Metric(**row))
            return m
        except sqlite3.Error:
            return Metrics()

    def get_component_pipelines(self, component: str) -> List[str]:
        query = "select distinct(json_extract(S.RUN_DESCRIPTION, '$.pipeline_branch')) as PIPELINES" \
                " from TEST_SESSIONS S, TEST_METRICS M " \
                " where json_extract(S.RUN_DESCRIPTION, '$.pipeline_branch') != '' and M.COMPONENT = ?"
        try:
            row = self.__cnx.execute(query, (component,)).fetchall()
            return [i['pipelines'] for i in row]
        except sqlite3.Error:
            return []

    def get_component_pipelines_build(self, component: str, pipeline: str) -> List[str]:
        query = "select distinct(json_extract(S.RUN_DESCRIPTION, '$.pipeline_build_no')) as BUILDS" \
                " from TEST_SESSIONS S, TEST_METRICS M " \
                " where M.COMPONENT = ? and json_extract(S.RUN_DESCRIPTION, '$.pipeline_branch') = ?"
        try:
            row = self.__cnx.execute(query, (component, pipeline)).fetchall()
            return [i['builds'] for i in row]
        except sqlite3.Error:
            return []

    def get_item_metrics(self, item: str) -> Metrics:
        self._set_tr_context('metric')
        res = Metrics()
        query = "select * from TEST_METRICS where ITEM = ?;"
        try:
            for row in self.__cnx.execute(query, (item,)).fetchall():
                m = Metric(**row)
                res.append(m)
            return res
        except sqlite3.Error:
            return Metrics()

    def get_metrics_of_variant(self, variant: str, component: str = None) -> Metrics:
        if component:
            query = 'SELECT * FROM TEST_METRICS WHERE ITEM_VARIANT = ? AND COMPONENT = ?'
            bind = (variant, component)
        else:
            query = 'SELECT * FROM TEST_METRICS WHERE ITEM_VARIANT = ?'
            bind = (variant,)
        m = Metrics()
        try:
            self._set_tr_context('metric')
            for row in self.__cnx.execute(query, bind).fetchall():
                m.append(Metric(**row))
            return m
        except sqlite3.Error:
            return Metrics()

    def get_context_details(self, context_h: str) -> Optional[Context]:
        self._set_tr_context('context')
        try:
            data = self.__cnx.execute('select * from EXECUTION_CONTEXTS where ENV_H = ?', (context_h,)).fetchone()
            return Context(**data) if data is not None else None
        except sqlite3.Error:
            return None

    def get_metrics_by_resource(self, resource: ResourceType, method: ResourceMethod = ResourceMethod.TOP,
                                max_element: int = 10) -> Metrics:
        if method == ResourceMethod.TOP:
            order_by_method = "DESC"
        else:
            order_by_method = "ASC"
        query = f'SELECT * from TEST_METRICS ORDER BY {resource.value} {order_by_method} LIMIT ?'
        metrics = Metrics()
        self._set_tr_context('metric')
        try:
            data = self.__cnx.execute(query, (max_element,))
            for metric in data.fetchall():
                metrics.append(Metric(**metric))
            return metrics
        except sqlite3.Error:
            return Metrics()

    def get_metrics_by_component_resource(self, resource: ResourceType, component: str,
                                          method: ResourceMethod = ResourceMethod.TOP,
                                          max_element: int = 10) -> Metrics:
        if method == ResourceMethod.TOP:
            order_by_method = f"DESC"
        else:
            order_by_method = f"ASC"
        query = f'SELECT * from TEST_METRICS WHERE COMPONENT=? ORDER BY {resource.value.upper()}' \
                f' {order_by_method} LIMIT ?'
        metrics = Metrics()
        self._set_tr_context('metric')
        try:
            for metric in self.__cnx.execute(query, (component, max_element)).fetchall():
                metrics.append(Metric(**metric))
            return metrics
        except sqlite3.Error:
            return Metrics()

    def get_metrics_by_pipeline_resource(self, resource: ResourceType, pipeline: str,
                                         method: ResourceMethod = ResourceMethod.TOP,
                                         max_element: int = 10) -> Metrics:
        if method == ResourceMethod.TOP:
            order_by_method = " DESC"
        else:
            order_by_method = " ASC"
        query = f'SELECT M.* from TEST_METRICS M, TEST_SESSIONS S' \
                f' WHERE json_extract(S.RUN_DESCRIPTION, "$.pipeline_branch") = ?' \
                f' AND M.SESSION_H = S.SESSION_H' \
                f' ORDER BY {resource.value.upper()}'
        query += f'{order_by_method} LIMIT ?'
        metrics = Metrics()
        self._set_tr_context('metric')
        try:
            for metric in self.__cnx.execute(query, (pipeline, max_element)).fetchall():
                metrics.append(Metric(**metric))
            return metrics
        except sqlite3.Error:
            return Metrics()

    def get_metrics_by_build_resource(self, resource: ResourceType, pipeline: str, build: str,
                                      method: ResourceMethod = ResourceMethod.TOP,
                                      max_element: int = 10) -> Metrics:
        if method == ResourceMethod.TOP:
            order_by_method = "DESC"
        else:
            order_by_method = "ASC"
        query = f'SELECT M.* from TEST_METRICS M, TEST_SESSIONS S' \
                f' WHERE json_extract(S.RUN_DESCRIPTION, "$.pipeline_branch") = ?' \
                f' AND json_extract(S.RUN_DESCRIPTION, "$.pipeline_build_no") = ?' \
                f' AND M.SESSION_H = S.SESSION_H' \
                f' ORDER BY {resource.value} {order_by_method} LIMIT ?'
        metrics = Metrics()
        self._set_tr_context('metric')
        try:
            for metric in self.__cnx.execute(query, (pipeline, build, max_element)).fetchall():
                metrics.append(Metric(**metric))
            return metrics
        except sqlite3.Error:
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
        s = Sessions()
        try:
            self._set_tr_context('session')
            query = "SELECT * FROM TEST_SESSIONS WHERE" \
                    " json_extract(RUN_DESCRIPTION, '$.pipeline_branch') = ? AND" \
                    " json_extract(RUN_DESCRIPTION, '$.pipeline_build_no') = ?"
            rows = self.__cnx.execute(query, (pipeline, build_id)).fetchall()
            for row in rows:
                s.add(Session(**row))
            return s
        except sqlite3.Error:
            return Sessions()
