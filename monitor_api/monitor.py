# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from monitor_api.enums import MetricScope, ResourceType, ResourceMethod
from monitor_api.core.collections import Metrics, Sessions, Contexts
from monitor_api.core.entities import Session, Context
from monitor_api.dialects.local import Local
from monitor_api.dialects.remote import Remote
import typing


class Monitor:
    """Interface for manipulating your collected metrics either from a local storage or a remote server.

    :param str url: The url to the server, or the path to the local database.
    :Keyword Arguments for Remote server:
        Please refer to the `requests's Session <https://docs.python-requests.org/en/latest/api/#request-sessions>`_ .
        for more details

    :Keyword Arguments for Local server:
        Please refer to `sqlite3 connections <https://docs.python.org/3/library/sqlite3.html#connection-objects>`_
        for more details
    """
    def __init__(self, url: str, **kwargs):
        """Construct a new interface with a monitor storage.
        """
        if url.startswith('http://') or url.startswith('https://'):
            self.__dial = Remote(url, **kwargs)
        else:
            self.__dial = Local(url, **kwargs)

    def count_components(self) -> int:
        """Count total number of non empty components.

        :return: The number of non empty components
        :rtype: int
        """
        return self.__dial.count_components()

    def list_components(self) -> typing.List[str]:
        """Read all non empty components.

        :return: a list of non empty components
        :rtype: list(str)
        """
        return self.__dial.get_components()

    def list_component_pipelines(self, component: str) -> typing.List[str]:
        """Read for known pipelines on a given component.

        :param str component: Component for which this query must be done
        :return: The list of pipelines affiliated with this component
        :rtype: list(str)
        """
        return self.__dial.get_component_pipelines(component)

    def list_component_pipeline_builds(self, component: str, pipeline: str) -> typing.List[str]:
        """Read for known build ids of a pipeline on a given component.
        This is handy if you want to filter out sessions for comparison purpose.

        :param str component: Component for which this query must be done
        :param str pipeline: Pipeline identifier
        :return: The list of build ids affiliated with the pair pipeline/component
        :rtype: list(str)
        """
        return self.__dial.get_component_pipelines_build(component, pipeline)

    def list_component_metrics(self, component: typing.Optional[str] = None) -> Metrics:
        """Read for all metrics refering to the given component.

        :param str component: Optional. Component name. If None, metrics without component will be searched for.
        :return: A list of metrics, all of them having the requested component.
        :rtype: monitor_api.core.collections.Metrics
        """
        return self.__dial.read_component_metrics(component)

    def count_contexts(self) -> int:
        """Count the number of context entries.

        :return: The number of different context entries
        :rtype: int
        """
        return self.__dial.count_contexts()

    def list_contexts(self) -> Contexts:
        """Read all contexts and extract them into a Dict like structure for further preprocessing.
        The reference key is their hash member.

        :return: All contexts object referenced by their hash value.
        :rtype: monitor_api.core.collections.Contexts
        """
        return self.__dial.get_contexts()

    def get_context(self, context_h: str) -> typing.Optional[Context]:
        """Read and extract a single context object from a hash value.

        :param context_h: hash value of the context you wish to retrieve.
        :type context_h: str
        :return: A context object if there is a match between your hash key and accessed set of context,
                 None otherwise.
        :rtype: None or monitor_api.core.entities.Context
        """
        return self.__dial.get_context_details(context_h)

    def list_context_metrics(self, context_h: str) -> Metrics:
        """Read and extract all metrics having the given context hash value.

        :param context_h: hash value of the context you wish to retrieve.
        :type context_h: str
        :return: A list of metrics, all of which having their context key equal to the given context hash value.
        :rtype: monitor_api.core.collections.Metrics
        """
        return self.__dial.get_metrics_with_context(context_h)

    def count_metrics(self, session_h: str = None, context_h: str = None, scm_ref: str = None) -> int:
        """Count the number of metrics under some conditions.
        If no condition is set, the total number of metrics is computed.
        If session_h is set, count all metrics having session_h as session reference.
        Otherwise, if context_h is set, count all metrics having context_h as context reference.
        Otherwise, if scm_ref is set, count all metrics having a session pointing to this scm reference.

        :param session_h: A full session reference.
        :type session_h: str
        :param context_h: A full context reference.
        :type context_h: str
        :param scm_ref: A full scm reference.
        :type scm_ref: str
        :return: A number greater of equal to 0, -1 in case of access error.
        :rtype: int
        """
        return self.__dial.count_metrics(session_h, context_h, scm_ref)

    def list_item_metrics(self, item: str) -> Metrics:
        """Read all metrics for the given test item, mixing variant metrics together if your test is parameterized.

        :param item: the name of the test for which metrics must be retrieved.
        :rtype item: str
        :return: A (possibly empty) list of metrics.
        :rtype: monitor_api.core.collections.Metrics
        """
        return self.__dial.get_item_metrics(item)

    def list_metrics(self) -> Metrics:
        """Read all metrics.

        :return: A (possibly empty) list of metrics.
        :rtype: monitor_api.core.collections.Metrics
        """
        return self.__dial.get_metrics()

    def list_metrics_by_type(self, metric_type: MetricScope) -> Metrics:
        """Read all metrics linked to the given type of metrics.

        :param metric_type: the type of the test entity (function, module or package).
        :rtype metric_type: MetricType
        :return: A (possibly empty) list of metrics.
        :rtype: monitor_api.core.collections.Metrics
        :note: metric_type value package is not supported for now.
        """
        return self.__dial.get_metrics_by_type(metric_type)

    def list_metrics_by_scm_id(self, scm_ref: str) -> Metrics:
        """Read all metrics having a session pointing to this scm reference.

        :param scm_ref: Your entire scm reference
        :rtype scm_ref: str
        :return: A (possibly empty) list of metrics.
        :rtype: monitor_api.core.collections.Metrics
        """
        return self.__dial.get_metrics_with_scm_ref(scm_ref)

    def list_metrics_from_pattern(self, item: str = None, variant: str = None) -> Metrics:
        """Read all metrics using a prefix expression on either the test function or its variant.

        :param item: Prefix of your item. Leave it None if you want to focus on variants.
        :rtype item: str
        :param variant: Prefix of your variant. Leave it None if you want to focus on item.
        :rtype variant: str
        :return: A (possibly empty) list of metrics.
        :rtype: monitor_api.core.collections.Metrics
        """
        return self.__dial.get_metrics_by_pattern(item, variant)

    def list_metrics_of_variant(self, variant: str, component: str = None) -> Metrics:
        """Read all metrics for the given test variant, with ability to restrict the view with the component.

        :param variant: the name of the test for which metrics must be retrieved.
        :rtype variant: str
        :param component: Component name. Enables component restriction if set.
        :rtype component: str
        :return: A (possibly empty) list of metrics.
        :rtype: monitor_api.core.collections.Metrics
        """
        return self.__dial.get_metrics_of_variant(variant, component)

    def count_sessions(self) -> int:
        """Count the number of session entries.

        :return: The number of different session entries
        :rtype: int
        """
        return self.__dial.count_sessions()

    def list_sessions(self, with_tags: typing.Union[str, typing.List[str]] = None,
                      restrict_flags: typing.Union[str, typing.List[str]] = None,
                      method: str = None) -> Sessions:
        """Read all sessions matching your criteria. If no filters are provided, all sessions are retrieved.

        :param with_tags: Set the tags you want your sessions must have.
        :type with_tags: either str or list(str)
        :param restrict_flags: restrict you tag's values. Must have same length has with_tags.
        :type restrict_flags: either str or list(str)
        :param method: indicates whether you want a strict match (match_all) or a permissive one (match_any)
        :type method: str (allowed values are match_all and match_any)
        :return: The list of sessions matching the conditions.
        :rtype: monitor_api.core.collections.Sessions
        :note: This interface is subject for change in future version!
        """
        return self.__dial.get_sessions(with_tags, restrict_flags, method)

    def list_session_metrics(self, session_h: str = None) -> Metrics:
        """Read all metrics having the given session reference.

        :param session_h: The full session reference
        :type session_h: str
        :return: A (possibly empty) list of metrics.
        :rtype: monitor_api.core.collections.Metrics
        """
        return self.__dial.get_metrics_by_session(session_h)

    def get_session(self, session_h: str) -> typing.Optional[Session]:
        """Retrieve the session object having the given session reference.

        :param session_h: The full session reference
        :type session_h: str
        :return: A session object if the provided reference has a match, None otherwise.
        :rtype: None or monitor_api.core.entities.Session
        """
        return self.__dial.get_session_details(session_h)

    def list_pipelines(self) -> typing.List[str]:
        """Retrieve the list of known pipelines

        :return: the list of pipeline names
        :rtype: list(str)
        """
        return self.__dial.get_pipelines()

    def list_pipeline_builds(self, pipeline: str) -> typing.List[str]:
        """For a given pipeline, list all known build identifiers.

        :param pipeline: The pipeline for which all build must be listed.
        :type pipeline: str
        :return: The list of builds associated to this pipeline
        :rtype: list(str)
        """
        return self.__dial.get_pipeline_builds(pipeline)

    def list_metrics_resources(self, resource: ResourceType, method: ResourceMethod,
                               max_element: int = 10) -> Metrics:
        """Retrieve metrics having the higher (resp. lower) resource consumption accross the whole sets of metrics.
        Operates on at most 500 entries.

        :param resource: The resource you want to operate the extraction on.
        :type resource: ResourceType
        :param method: Indicate if you want greediest or most disciplined tests.
        :type method: ResourceType
        :param max_element: Set the number of element you wish to retrieve. Default is 10.
        :type max_element: int
        :return: A (possibly empty) list of metrics.
        :rtype: monitor_api.core.collections.Metrics
        """
        return self.__dial.get_metrics_by_resource(resource, method, max_element)

    def list_metrics_resources_from_component(self, component: str, resource: ResourceType,
                                              method: ResourceMethod, max_element: int = 10) -> Metrics:
        """Retrieve metrics having the higher (resp. lower) resource consumption for a given component.
        Operates on at most 500 entries.

        :param component: A valid component identifier
        :type component: str
        :param resource: The resource you want to operate the extraction on.
        :type resource: ResourceType
        :param method: Indicate if you want greediest or most disciplined tests.
        :type method: ResourceType
        :param max_element: Set the number of element you wish to retrieve. Default is 10.
        :type max_element: int
        :return: A (possibly empty) list of metrics.
        :rtype: monitor_api.core.collections.Metrics
        """
        return self.__dial.get_metrics_by_component_resource(resource, component, method, max_element)

    def list_metrics_resources_from_pipeline(self, pipeline: str, resource: ResourceType,
                                             method: ResourceMethod, max_element: int = 10) -> Metrics:
        """Retrieve metrics having the higher (resp. lower) resource consumption accross a pipeline (multiple builds).
        Operates on at most 500 entries.

        :param pipeline: The pipeline name of the build.
        :type pipeline: str
        :param resource: The resource you want to operate the extraction on.
        :type resource: ResourceType
        :param method: Indicate if you want greediest or most disciplined tests.
        :type method: ResourceType
        :param max_element: Set the number of element you wish to retrieve. Default is 10.
        :type max_element: int
        :return: A (possibly empty) list of metrics.
        :rtype: monitor_api.core.collections.Metrics
        """
        return self.__dial.get_metrics_by_pipeline_resource(resource, pipeline, method, max_element)

    def list_metrics_resources_from_build(self, pipeline: str, build: str, resource: ResourceType,
                                          method: ResourceMethod, max_element: int = 10) -> Metrics:
        """Retrieve metrics having the higher (resp. lower) resource consumption for a full build reference.
        Operates on at most 500 entries.

        :param pipeline: The pipeline name of the build.
        :type pipeline: str
        :param build: The build identifier
        :type build: str
        :param resource: The resource you want to operate the extraction on.
        :type resource: ResourceType
        :param method: Indicate if you want greediest or most disciplined tests.
        :type method: ResourceType
        :param max_element: Set the number of element you wish to retrieve. Default is 10.
        :type max_element: int
        :return: A (possibly empty) list of metrics.
        :rtype: monitor_api.core.collections.Metrics
        """
        return self.__dial.get_metrics_by_build_resource(resource, pipeline, build, method, max_element)

    def list_metrics_from(self, sessions: Sessions = None, contexts: Context = None) -> Metrics:
        """For sessions and contexts, retrieve all metrics referencing at least a session or a context.

        :param sessions: Your set of sessions
        :type sessions: Sessions
        :param contexts: Your set of contexts
        :type contexts: Contexts
        :return: A (possibly empty) list of metrics
        :rtype: monitor_api.core.collections.Metrics
        """
        return self.__dial.get_metrics_from(sessions, contexts)

    def list_sessions_from(self, metrics: Metrics) -> Sessions:
        """Retrieve all sessions referenced in the metrics set.

        :param metrics: A set of metrics
        :type metrics: Metrics
        :return: All sessions object reference in your Metrics object.
        :rtype: monitor_api.core.collections.Sessions
        """
        return self.__dial.get_sessions_from(metrics)

    def list_contexts_from(self, metrics: Metrics) -> Contexts:
        """Retrieve all contexts referenced in the metrics set.

        :param metrics: A set of metrics
        :type metrics: Metrics
        :return: All context objects reference in your Metrics object.
        :rtype: monitor_api.core.collections.Contexts
        """
        return self.__dial.get_contexts_from(metrics)

    def list_build_sessions(self, pipeline: str, build_id: str) -> Sessions:
        """Retrieve all sessions for the given pipeline and build identifier.

        :param pipeline: The pipeline identifier
        :type pipeline: str
        :param build_id: The build identifier
        :type build_id: str
        :return: All session objects for the given build.
        :rtype: monitor_api.core.collections.Sessions
        """
        return self.__dial.get_sessions_from_build(pipeline, build_id)
