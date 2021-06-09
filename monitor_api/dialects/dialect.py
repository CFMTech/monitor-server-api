# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from monitor_api.enums import MetricScope, ResourceType, ResourceMethod
from monitor_api.core.entities import Context, Session
from monitor_api.core.collections import Contexts, Metrics, Sessions
from typing import Optional, List, Union
import abc


class Dialect:  # pragma: no cover
    @abc.abstractmethod
    def get_sessions(self, with_tags: Union[str, List[str]] = None,
                     restrict_flags: Union[str, List[str]] = None,
                     method: str = None) -> Sessions:
        raise NotImplementedError

    @abc.abstractmethod
    def get_metrics(self) -> Metrics:
        raise NotImplementedError

    @abc.abstractmethod
    def get_metrics_with_context(self, context_h: str) -> Metrics:
        raise NotImplementedError

    @abc.abstractmethod
    def get_metrics_with_scm_ref(self, scm_ref: str) -> Metrics:
        raise NotImplementedError

    @abc.abstractmethod
    def get_metrics_by_type(self, metric_type: MetricScope) -> Metrics:
        raise NotImplementedError

    @abc.abstractmethod
    def get_metrics_by_pattern(self, item: str = None, variant: str = None) -> Metrics:
        raise NotImplementedError

    @abc.abstractmethod
    def get_metrics_by_session(self, session_h: str) -> Metrics:
        raise NotImplementedError

    @abc.abstractmethod
    def get_components(self) -> List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_contexts(self) -> Contexts:
        raise NotImplementedError

    @abc.abstractmethod
    def count_components(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def count_contexts(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def count_metrics(self, session_h: str = None, context_h: str = None, scm_ref: str = None) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def count_sessions(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get_session_details(self, session_h) -> Optional[Session]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_pipelines(self) -> List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_pipeline_builds(self, pipeline: str) -> List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def read_component_metrics(self, component: Optional[str] = None) -> Metrics:
        raise NotImplementedError

    @abc.abstractmethod
    def get_component_pipelines(self, component: str) -> List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_component_pipelines_build(self, component: str, pipeline: str) -> List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_item_metrics(self, item: str) -> Metrics:
        raise NotImplementedError

    @abc.abstractmethod
    def get_context_details(self, context_h: str) -> Optional[Context]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_metrics_by_resource(self, resource: ResourceType, method: ResourceMethod = ResourceMethod.TOP,
                                max_element: int = 10) -> Metrics:
        raise NotImplementedError

    @abc.abstractmethod
    def get_metrics_by_component_resource(self, resource: ResourceType,  component: str,
                                          method: ResourceMethod = ResourceMethod.TOP,
                                          max_element: int = 10) -> Metrics:
        raise NotImplementedError

    @abc.abstractmethod
    def get_metrics_by_pipeline_resource(self, resource: ResourceType,  pipeline: str,
                                         method: ResourceMethod = ResourceMethod.TOP,
                                         max_element: int = 10) -> Metrics:
        raise NotImplementedError

    @abc.abstractmethod
    def get_metrics_by_build_resource(self, resource: ResourceType, pipeline: str, build: str,
                                      method: ResourceMethod = ResourceMethod.TOP,
                                      max_element: int = 10) -> Metrics:
        raise NotImplementedError

    @abc.abstractmethod
    def get_metrics_from(self, sessions: Sessions = None, contexts: Contexts = None) -> Metrics:
        raise NotImplementedError

    @abc.abstractmethod
    def get_metrics_of_variant(self, variant: str, component: str = None) -> Metrics:
        raise NotImplementedError

    @abc.abstractmethod
    def get_sessions_from_build(self, pipeline: str, build_id: str) -> Sessions:
        raise NotImplementedError
