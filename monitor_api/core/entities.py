# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from monitor_api.enums import Field, MetricScope, CONTEXT_ALL_FIELDS, METRIC_ALL_FIELDS, SESSION_ALL_FIELDS
import datetime
from typing import List, Union, Dict, Optional
import hashlib


class Metric:
    """Basic metric record.

    :param context_h: Context identifier.
    :type context_h: str
    :param session_h: Session identifier.
    :type session_h: str
    :param start_time: Time at which the metrics have been registered (in ISO format).
    :type context_h: str
    :param item_path: Python like path to the item (with eventual modules).
    :type item_path: str
    :param item: Test item name.
    :type item: str
    :param variant: Full item qualified identifier.
    :type variant: str
    :param path: Path on the filesystem to the module containing the test item.
    :type path: str
    :param kind: Metric's scope (function, module).
    :type kind: str
    :param component: Logical system to which the test belongs.
    :type component: str
    :param wall_time: Total time spent running the test.
    :type wall_time: float
    :param user_time: Time spent running the test in user mode.
    :type user_time: float
    :param kernel_time: Time spent running the test in kernel mode.
    :type kernel_time: float
    :param cpu_usage: Cpu usage while running the test.
    :type cpu_usage: float
    :param memory_usage: Total memory used by the test.
    :type memory_usage: float
    """
    def __init__(self, context_h: str = None, session_h: str = None, start_time: str = None,
                 item_path: str = None, item: str = None, variant: str = None, path: str = None,
                 kind: MetricScope = None, component: str = None, wall_time: float = None, user_time: float = None,
                 kernel_time: float = None, cpu_usage: float = None, memory_usage: float = None):
        self.__c_h = context_h or ''
        self.__s_h = session_h or ''
        self.__time = datetime.datetime.fromisoformat(start_time)
        self.__item_path = item_path or ''
        self.__item = item or ''
        self.__variant = variant or ''
        self.__path = path or ''
        self.__kind = MetricScope.FUNCTION if kind is None else kind
        self.__component = component or ''
        self.__wall = wall_time or 0.0
        self.__user = user_time or 0.0
        self.__kernel = kernel_time or 0.0
        self.__cpu = cpu_usage or 0.0
        self.__memory = memory_usage or 0.0

    def is_function(self):
        """Test if the metric scope is positioned to FUNCTION.

        :return: True if the metric concerns a test function
        :rtype: bool
        """
        return self.__kind == MetricScope.FUNCTION

    def is_package(self):
        """Test if the metric scope is positioned to PACKAGE.

        :return: True if the metric concerns a test package
        :rtype: bool
        """
        return self.__kind == MetricScope.PACKAGE

    def is_module(self):
        """Test if the metric scope is positioned to MODULE.

        :return: True if the metric concerns a test module
        :rtype: bool
        """
        return self.__kind == MetricScope.MODULE

    @property
    def context(self) -> str:
        """Retrieves the context identifier linked to this metric.

        :return: A context identifier
        :rtype: str
        """
        return self.__c_h

    @property
    def session(self) -> str:
        """Retrieves the session identifier linked to this metric.

        :return: A session identifier
        :rtype: str
        """
        return self.__s_h

    @property
    def run_time(self) -> datetime.datetime:
        """Provide the time at which the metrics have been measured.

        :return: A date time expressed in UTC Coordinates.
        :rtype: datetime.datetime
        """
        return self.__time

    @property
    def item_path(self) -> str:
        """Python path like string to the object.

        :return: An import path
        :rtype: str
        """
        return self.__item_path

    @property
    def path(self) -> str:
        """Retrieves the test path relatively to current working directory where pytest has run.

        :return: A path
        :rtype: str
        """
        return self.__path

    @property
    def item(self) -> str:
        """Retrieves the test item name.
        If you want the test identifier, you should rather consider variant.
        Note that this might not be sufficient if multiple components have items named the same way.

        :return: The test item.
        :rtype: str
        """
        return self.__item

    @property
    def variant(self) -> str:
        """Retrieves the fully qualified test name, including parameter values if any.

        :return: A test identifier
        :rtype: str
        """
        return self.__variant

    @property
    def scope(self) -> MetricScope:
        """Retrieves the metrics scope (function, module or package).

        :return: the test scope
        :rtype: `monitor_api.MetricScope`
        """
        return self.__kind

    @property
    def component(self) -> str:
        """Retrieves the test component. Components can be viewed as a logical system representing
        an application or a subsystem.

        :return: the test's component name.
        :rtype: str
        """
        return self.__component

    @property
    def wall_time(self) -> float:
        """Retrieves the total, real time spent running the test.
        The unit is the second.

        :return: Time spent running the test.
        :rtype: float
        """
        return self.__wall

    @property
    def user_time(self) -> float:
        """Retrieves the amount of time spent running the test in user mode.
        The unit is the second.

        :return: Time spent running in user mode.
        :rtype: float
        """
        return self.__user

    @property
    def kernel_time(self) -> float:
        """Retrieves the amount of time spent running in kernel mode.
        The unit is the second.

        :return: Time spent running in kernel mode.
        :rtype: float
        """
        return self.__kernel

    @property
    def cpu_usage(self) -> float:
        """Retrieves the cpu usage (in percentage) of the test.

        Example
          -  0.6577 means 65.77 % use of a single CPU.
          -  3.768 means 3 CPU at 100 % plus another one at 76.8 %.

        :return: The test's cpu usage.
        :rtype: float
        """
        return self.__cpu

    @property
    def memory_usage(self) -> float:
        """Retrieves the amount of memory used by the test.
        The unit is the MB.

        :return: Memory used (in MB)
        :rtype: float
        """
        return self.__memory

    def to_dict(self, keep: List[Field] = None, drop: List[Field] = None) -> dict:
        """Convert the instance to a dictionary for further use. You can control which field
        will be exported using a keep/drop approach. Note that controlling the export can only be
        done using either `keep` or `drop` parameter.

        :param keep: List of field to keep. Use it if the field you want to focus on is small.
        :param drop: List of field to drop. Use it if the field you want to focus on is long.
        :type keep: list(`monitor_api.Field`)
        :type drop: list(`monitor_api.Field`)
        :return: A dictionary containing members whitelisted for export.
        :rtype: dict
        """
        d = {Field.CONTEXT_H.value: self.context,
             Field.SESSION_H.value: self.session,
             Field.ITEM_START_TIME.value: self.run_time,
             Field.ITEM_PATH.value: self.item_path,
             Field.ITEM.value: self.item,
             Field.ITEM_FS_LOC.value: self.path,
             Field.ITEM_VARIANT.value: self.variant,
             Field.KIND.value: self.scope.value,
             Field.TOTAL_TIME.value: self.wall_time,
             Field.USER_TIME.value: self.user_time,
             Field.KERNEL_TIME.value: self.kernel_time,
             Field.CPU_USAGE.value: self.cpu_usage,
             Field.MEM_USAGE.value: self.memory_usage,
             Field.COMPONENT.value: self.component}

        if keep is not None:
            cols = [col for col in METRIC_ALL_FIELDS if col not in keep]
        elif drop is not None:
            cols = [col for col in METRIC_ALL_FIELDS if col in drop]
        else:
            cols = []

        for col in cols:
            del d[col.value]
        return d

    def hash(self):
        """ Emulate hash key to avoid the same metric to be inserted multiple times
        in Metrics resource (useful for some entry points).

        :return: A hash key that uniquely identifies the test.
        :rtype: str
        """
        hr = hashlib.sha256()
        hr.update(self.context.encode())
        hr.update(self.session.encode())
        hr.update(self.run_time.isoformat().encode())
        hr.update(self.item_path.encode())
        hr.update(self.item.encode())
        hr.update(self.path.encode())
        hr.update(self.variant.encode())
        hr.update(self.scope.name.encode())
        hr.update(self.component.encode())
        hr.update(str(self.wall_time).encode())
        hr.update(str(self.user_time).encode())
        hr.update(str(self.kernel_time).encode())
        hr.update(str(self.cpu_usage).encode())
        hr.update(str(self.memory_usage).encode())
        return hr.hexdigest()


class Context:
    """Single execution context record. This is basically the machine which executed tests.

    :param h: Context identifier.
    :type h: str
    :param cpu_count: Number of CPU on the machine
    :type cpu_count: int
    :param cpu_freq: Nominal frequency of the CPI
    :type cpu_freq: int
    :param cpu_type: Architecture of the CPU
    :type cpu_type: str
    :param cpu_vendor: The CPU Vendor. Optional.
    :type cpu_vendor: str
    :param ram_total: Total amount of physical RAM available on the machine.
    :type ram_total: int
    :param mac_node: Fully qualified domain name of the machine.
    :type mac_node: str
    :param mac_type: Machine/OS type
    :type mac_type: str
    :param mac_arch: Machine architecture (32 or 64bits)
    :type mac_arch: str
    :param sys_info: OS kernel information.
    :type sys_info: str
    :param py_info: Python information.
    :type py_info: str
    """
    def __init__(self, h: str = None, cpu_count: int = None, cpu_freq: int = None, cpu_type: str = None,
                 cpu_vendor: str = None, ram_total: int = None, mac_node: str = None, mac_type: str = None,
                 mac_arch: str = None, sys_info: str = None, py_info: str = None):
        self.__h = h or ''
        self.__cpu_count = cpu_count or 1
        self.__cpu_freq = cpu_freq or 0
        self.__cpu_type = cpu_type or ''
        self.__cpu_vendor = cpu_vendor or ''
        self.__ram = ram_total or 0
        self.__mac_node = mac_node or ''
        self.__mac_type = mac_type or ''
        self.__mac_arch = mac_arch or ''
        self.__sys = sys_info or ''
        self.__py = py_info or ''

    @property
    def h(self) -> str:
        """Context identifier. Unique across all contexts. If two identifiers share the same
        value, it means that they point to objects with similar values.

        :return: A unique key for referencing this context.
        :rtype: str
        """
        return self.__h

    @property
    def cpu_count(self) -> int:
        """Total number of CPU on the machine.

        :return: The number of CPU on the machine
        :rtype: int
        """
        return self.__cpu_count

    @property
    def cpu_freq(self) -> int:
        """Nominal CPU frequency on the machine. Expressed in MHz

        :return: The CPU frequency expressed in MHz.
        :rtype: int
        """
        return self.__cpu_freq

    @property
    def cpu_type(self) -> str:
        """Architecture of the CPU.

        :return: Architecture identifier string.
        :rtype: str
        """
        return self.__cpu_type

    @property
    def cpu_vendor(self) -> str:
        """CPU model name, as provided by vendor.

        :return: CPU brand name
        :rtype: str
        """
        return self.__cpu_vendor

    @property
    def total_ram(self) -> int:
        """Total amount of RAM available on the machine, expressed in MB.

        :return: The amount of RAM (in MB)
        :rtype: int
        """
        return self.__ram

    @property
    def machine_node(self) -> str:
        """The machine fully qualified domain name.

        :return: the machine hostname.
        :rtype: str
        """
        return self.__mac_node

    @property
    def machine_type(self) -> str:
        """The machine type details the instruction set supported by the processor.

        :return: the machine type.
        :rtype: str
        """
        return self.__mac_type

    @property
    def machine_arch(self) -> str:
        """The machine architecture (32 or 64 bits).

        :return: the machine bitmode.
        :rtype: str
        """
        return self.__mac_arch

    @property
    def sys_info(self) -> str:
        """A string detailing some information about the OS kernel.
        Can explain the exact version of the kernel.

        :return: A informative string about the OS kernel.
        :rtype: str
        """
        return self.__sys

    @property
    def python_info(self) -> str:
        """A string detailing some information about the version of Python used for testing.
        Can explain how the interpreter has been compiled, on which system and when.

        :return: A informative string about the python interpreter.
        :rtype: str
        """
        return self.__py

    def to_dict(self, keep: List[Field] = None, drop: List[Field] = None) -> dict:
        """Convert the instance to a dictionary for further use. You can control which field
        will be exported using a keep/drop approach. Note that controlling the export can only be
        done using either `keep` or `drop` parameter.

        :param keep: List of field to keep. Use it if the field you want to focus on is small.
        :param drop: List of field to drop. Use it if the field you want to focus on is long.
        :type keep: list(`monitor_api.Field`)
        :type drop: list(`monitor_api.Field`)
        :return: A dictionary containing members whitelisted for export
        :rtype: dict
        """
        d = {Field.CONTEXT_H.value: self.h,
             Field.CPU_COUNT.value: self.cpu_count,
             Field.CPU_FREQUENCY_MHZ.value: self.cpu_freq,
             Field.CPU_TYPE.value: self.cpu_type,
             Field.CPU_VENDOR.value: self.cpu_vendor,
             Field.MACHINE_ARCH.value: self.machine_arch,
             Field.MACHINE_NODE.value: self.machine_node,
             Field.MACHINE_TYPE.value: self.machine_type,
             Field.RAM_TOTAL_MB.value: self.total_ram,
             Field.SYSTEM_INFO.value: self.sys_info,
             Field.PYTHON_INFO.value: self.python_info}

        if keep is not None:
            cols = [col for col in CONTEXT_ALL_FIELDS if col not in keep]
        elif drop is not None:
            cols = [col for col in CONTEXT_ALL_FIELDS if col in drop]
        else:
            cols = []

        for col in cols:
            del d[col.value]
        return d


class Session:
    """A session record. Contains SCM reference, start date and tags.

    :param h: session identifier
    :type h: str
    :param scm_ref: Source code management reference
    :type scm_ref: str
    :param run_date: Date time at which the session has been started.
    :type run_date: str
    :param tags: Additional tags used for identifying special run conditions.
    :type tags: dict
    """
    def __init__(self, h: str = None, scm_ref: str = None,
                 run_date: str = None,
                 tags: Optional[Union[Dict[str, str], List[Dict[str, str]]]] = None):
        self.__h = h or ''
        self.__scm = scm_ref or ''
        self.__start_date = datetime.datetime.fromisoformat(run_date)
        self.__tags = tags or dict()
        if type(tags) is list:
            # We try to map to a session sent by remote server
            try:
                d = dict()
                for item in tags:
                    d[item['name']] = item['value']
                self.__tags = d
            except KeyError:
                self.__tags = dict()

    def __str__(self):
        tags = None
        if self.__tags:
            tags = [f'        - {k}: {v}' for k, v in self.__tags.items()]
            tags = '\n'.join(tags)
        if tags is None:
            return f'''{self.__h}:
    run_date: {self.__start_date}
    scm: {self.__scm}
'''
        else:
            return f'''{self.__h}:
    run_date: {self.__start_date}
    scm: {self.__scm}
    tags:
{tags}
'''

    @property
    def tags(self) -> dict:
        """Retrieves all tags set on this session.
        All tags have their values represented as string.

        :return: A dictionary with key as tags and values as tag's value.
        :rtype: dict[str, str]
        """
        return self.__tags

    @property
    def h(self) -> str:
        """Session identifier. Unique across all sessions. If two identifiers share the same
        value, it means that they point to objects with similar values.

        :return: A unique key for referencing this session.
        :rtype: str
        """
        return self.__h

    @property
    def scm(self) -> str:
        """SCM reference to the code which have been executed.

        :return: A SCM reference
        :rtype: str"""
        return self.__scm

    @property
    def start_date(self) -> datetime.datetime:
        """Retrieve the start date at which the test session has started.

        :return: A datetime object positioned at the time the session started.
        :rtype: datetime.datetime
        """
        return self.__start_date

    def to_dict(self, keep: List[Field] = None, drop: List[Field] = None,
                expand_tags: bool = False) -> dict:
        """Convert the instance to a dictionary for further use. You can control which field
        will be exported using a keep/drop approach. Tags can be exported using an expand strategy
        and if requested, each tag is exported as if it was a real session field. This means that
        the final dictionary will have a depth of 1.
        Otherwise, tags will be grouped under a 'tags' element thus giving access to a sub dictionary
        containing all tags and only all tags. In this case, the final dictionary will have a depth of 2.

        Note that controlling the export can only be done using either `keep` or `drop` parameter.

        :param keep: List of field to keep. Use it if the field you want to focus on is small.
        :type keep: list(`monitor_api.Field`)
        :param drop: List of field to drop. Use it if the field you want to focus on is long.
        :type drop: list(`monitor_api.Field`)
        :param expand_tags: control how tags are exported. If set to True, tags will be exported like other
                            session members.
        :type expand_tags: bool
        :return: A dictionary containing members whitelisted for export
        :rtype: dict
        """
        if not expand_tags:
            d = {Field.SESSION_H.value: self.h,
                 Field.RUN_DATE.value: self.start_date,
                 Field.SCM.value: self.scm,
                 Field.TAGS.value: self.tags}
        else:
            d = {Field.SESSION_H.value: self.h,
                 Field.RUN_DATE.value: self.start_date,
                 Field.SCM.value: self.scm}
            d.update(self.tags)

        # If expand_tags, we keep (resp. drop) all tag fields
        dk_tags = list(set(d.keys()).difference(set([f.value for f in SESSION_ALL_FIELDS])))
        cols = []
        if keep is not None:
            cols = [col.value for col in SESSION_ALL_FIELDS if col not in keep]
            if expand_tags and Field.TAGS.value in cols:
                cols.remove(Field.TAGS.value)
                cols.extend(dk_tags)
        elif drop is not None:
            cols = [col.value for col in SESSION_ALL_FIELDS if col in drop]
            if expand_tags and Field.TAGS.value in cols:
                cols.remove(Field.TAGS.value)
                cols.extend(dk_tags)

        for col in cols:
            del d[col]
        return d
