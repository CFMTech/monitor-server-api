# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from monitor_api.enums import Field
from monitor_api.core.entities import Context, Metric, Session
import collections
import pandas as pd
import typing
import yaml


class Contexts(collections.UserDict):
    """Dict like structure for manipulating `monitor_api.core.entities.Context` objects."""
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add(self, context: Context) -> Context:
        """Add a context object to this collection.

        :param context: Context object to add. As for dictionaries, overwrites any existing entry with equivalent hash.
        :type context: monitor_api.core.entities.Context
        :return: The object which have been added
        :rtype: monitor_api.core.entities.Context
        """
        self[context.h] = context
        return context

    def filter_with(self, cond: typing.Callable[[Context], bool], inplace: bool = False):
        """Apply a filter to the bag of `monitor_api.core.entities.Context` held by the instance
        calling this method. Only `monitor_api.core.entities.Context` objects matching the condition method
        are kept.

        :param cond: A callable returning a boolean (True means keep) with a unique parameter of type
                     `monitor_api.core.entities.Context`
        :type cond: Callable[[`monitor_api.core.entities.Context`], bool]
        :param inplace: If True, change the content of this instance by keeping only values for which cond is True
        :type inplace: bool
        :return: The object itself
        :rtype: `monitor_api.core.collections.Contexts`
        """
        c = Contexts()
        for context in self.data.values():
            if cond(context):
                c[context.h] = context
        if inplace:
            self.data = c.data
            return self
        return c

    def to_df(self, keep: typing.List[Field] = None, drop: typing.List[Field] = None) -> pd.DataFrame:
        """Turn a collection of `monitor_api.core.entities.Context` into a pandas DataFrame.

         You can keep or drop a given list of `monitor_api.Field` by specifying either *keep* or
         *drop* as a parameter. If both are provided, *keep* will be used instead of *drop*.

        :param keep: List of field to keep during the export. Cannot be used conjointly with *drop*
        :type keep: list(`monitor_api.Field`)
        :param drop: List of field to keep during the export. Cannot be used conjointly with *keep*
        :type drop: list(`monitor_api.Field`)
        :return: A valid pandas DataFrame object representing the collection of this instance, without any
                 index set minus eventual information that might have been marked as dropped.
        :rtype: pandas.DataFrame
        """
        d = []
        for c in self.data.values():
            d.append(c.to_dict(keep=keep, drop=drop))
        return pd.DataFrame(d)

    def __str__(self):
        d = dict(contexts=self.data)
        for i, c in enumerate(self.data.values()):
            cd = c.to_dict()
            d['contexts'][cd['context_h']] = cd
            del d['contexts'][cd['context_h']]['context_h']
        return yaml.dump(d)


class Sessions(collections.UserDict):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add(self, session: Session) -> Session:
        """Add a session object to this collection.

        :param session: Session object to add. As for dictionaries, overwrites any existing entry with equivalent hash.
        :type session: monitor_api.core.entities.Session
        :return: The object which have been added
        :rtype: monitor_api.core.entities.Session
        """
        self[session.h] = session
        return session

    def filter_with(self, cond: typing.Callable[[Session], bool], inplace: bool = False):
        """Apply a filter to the bag of `monitor_api.core.entities.Session` held by the instance
        calling this method. Only `monitor_api.core.entities.Session` objects matching the condition method
        are kept.

        :param cond: A callable returning a boolean (True means keep) with a unique parameter of type
                     `monitor_api.core.entities.Session`
        :type cond: Callable[[`monitor_api.core.entities.Session`], bool]
        :param inplace: If True, change the content of this instance by keeping only values for which cond is True
        :type inplace: bool
        :return: The object itself
        :rtype: `monitor_api.core.collections.Sessions`
        """
        s = Sessions()
        for session in self.data.values():
            if cond(session):
                s[session.h] = session
        if inplace:
            self.data = s.data
            return self
        return s

    def with_scm(self, scm: str):
        """Performs a filter operation in order to get a new collection with only session objects with the requested
           source code reference.

           :param scm: The source code reference to use for filter operation
           :type scm: str
           :return: A new Sessions object holding only sessions with scm reference set to the requested one.
           :rtype: monitor_api.core.collections.Sessions
        """
        s = Sessions()
        for session in self.data.values():
            if session.scm == scm:
                s[session.h] = session
        return s

    def with_tags(self, *args, **kwargs):
        """Performs a filter operation in order to get a new collection with only session objects with the requested
           tag specification. You can query for tag presence and/or tag value

           :param args: The list of tags to query for presence
           :type args: list[str]
           :param kwargs: Dictionary of tags to query for their values.
           :return: A new Sessions object holding only sessions matching the specified tag requirements.
           :rtype: monitor_api.core.collections.Sessions
        """
        coll = Sessions()
        for session in self.data.values():
            insert_ok = True
            for tag in args:
                if tag not in session.tags:
                    insert_ok = False
                    break
            for tag, value in kwargs.items():
                if tag not in session.tags:
                    insert_ok = False
                    break
                else:
                    if session.tags[tag] != value:
                        insert_ok = False
                        break
            if insert_ok and (args or kwargs):
                coll[session.h] = session
        return coll

    def to_df(self, keep: typing.List[Field] = None, drop: typing.List[Field] = None) -> pd.DataFrame:
        """Turn a collection of `monitor_api.core.entities.Session` into a pandas DataFrame.

         You can keep or drop a given list of `monitor_api.Field` by specifying either *keep* or
         *drop* as a parameter. If both are provided, *keep* will be used instead of *drop*.
         Tags are exported (if requested) using the expand strategy (see `monitor_api.core.entities.Session.to_dict`
         for more details)

        :param keep: List of field to keep during the export. Cannot be used conjointly with *drop*
        :type keep: list(`monitor_api.Field`)
        :param drop: List of field to keep during the export. Cannot be used conjointly with *keep*
        :type drop: list(`monitor_api.Field`)
        :return: A valid pandas DataFrame object representing the collection of this instance, without any
                 index set minus eventual information that might have been marked as dropped.
        :rtype: pandas.DataFrame
        """
        d = []
        for s in self.data.values():
            d.append(s.to_dict(keep=keep, drop=drop, expand_tags=True))
        return pd.DataFrame(d)

    def __str__(self):
        d = dict(sessions=dict())
        for s in self.data.values():
            sd = s.to_dict()
            d['sessions'][sd['session_h']] = sd
            if not d['sessions'][sd['session_h']]['tags']:
                del d['sessions'][sd['session_h']]['tags']
            del d['sessions'][sd['session_h']]['session_h']
        return yaml.dump(d)


class Metrics(collections.UserList):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def filter_with(self, cond: typing.Callable[[Metric], bool], inplace: bool = False):
        """Apply a filter to the bag of `monitor_api.core.entities.Metric` held by the instance
        calling this method. Only `monitor_api.core.entities.Metric` objects matching the condition method
        are kept.

        :param cond: A callable returning a boolean (True means keep) with a unique parameter of type
                     `monitor_api.core.entities.Metric`
        :type cond: Callable[[`monitor_api.core.entities.Metric`], bool]
        :param inplace: If True, change the content of this instance by keeping only values for which cond is True
        :type inplace: bool
        :return: The object itself
        :rtype: `monitor_api.core.collections.Metrics`
        """
        m = Metrics()
        for metric in self.data:
            if cond(metric):
                m.append(metric)
        if inplace:
            self.data = m.data
            return self
        return m

    def variants_of(self, item: str):
        """Performs a filter operation in order to get a new collection with only metric objects regarding any
           variant of the provided item.

           :param item: The test item for which you want to collect all variants known by this collection.
           :type item: str
           :return: A new Metrics object holding only metrics concerning a variant of the provided item.
           :rtype: monitor_api.core.collections.Metrics
        """
        m = Metrics()
        for metric in self.data:
            if metric.item == item:
                m.append(metric)
        return m

    def to_df(self, sessions: Sessions = None, contexts: Contexts = None,
              keep: typing.List[Field] = None, drop: typing.List[Field] = None) -> pd.DataFrame:
        """Turn a collection of `monitor_api.core.entities.Session` into a pandas DataFrame.

         You can keep or drop a given list of `monitor_api.Field` by specifying either *keep* or
         *drop* as a parameter. If both are provided, *keep* will be used instead of *drop*.

        :param sessions:
        :type sessions:
        :param contexts:
        :type contexts:
        :param keep: List of field to keep during the export. Cannot be used conjointly with *drop*
        :type keep: list(`monitor_api.Field`)
        :param drop: List of field to keep during the export. Cannot be used conjointly with *keep*
        :type drop: list(`monitor_api.Field`)
        :return: A valid pandas DataFrame object representing the collection of this instance, without any
                 index set minus eventual information that might have been marked as dropped.
        :rtype: pandas.DataFrame
        """

        d = []
        for m in self.data:
            v = m.to_dict(keep=keep, drop=drop)
            if sessions:
                v.update(sessions[m.session].to_dict(keep=keep, drop=drop, expand_tags=True))
            if contexts:
                v.update(contexts[m.context].to_dict(keep=keep, drop=drop))
            d.append(v)
        df = pd.DataFrame(d)
        return df

    @staticmethod
    def merge(metric_collection_r, metric_collection_l):
        """Merge two collection of metrics and ensure that no duplicate remains in the resulting collection.

        :param metric_collection_r: First collection to merge
        :param metric_collection_l: Second collection to merge
        :type metric_collection_l: monitor_api.core.collections.Metrics
        :type metric_collection_r: monitor_api.core.collections.Metrics
        :return: A new collection without duplicates.
        :rtype: monitor_api.core.collections.Metrics
        """
        processed = set()
        m = Metrics()
        for collection in (metric_collection_l, metric_collection_r):
            for metric in collection:
                key = metric.hash()
                if key not in processed:
                    m.append(metric)
                    processed.add(key)
        return m

    def unique(self, inplace: bool = False):
        """Filter the collection so that no duplicated metric remains.

        :param inplace: Modify this collection so that duplicates are removed.
        :type inplace: bool
        :return: A new collection without duplicates.
        :rtype: monitor_api.core.collections.Metrics
        """
        processed = set()
        m = Metrics()
        for metric in self.data:
            key = metric.hash()
            if key not in processed:
                m.append(metric)
                processed.add(key)
        if inplace:
            self.data = m.data
            return self
        return m

    def __str__(self):
        d = dict(metrics=dict())
        for i, m in enumerate(self.data):
            md = m.to_dict()
            d['metrics'][f'metric_{i}'] = md
        return yaml.dump(d)
