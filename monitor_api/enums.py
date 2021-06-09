# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT


import enum


class MetricScope(enum.Enum):
    """Represent the level at which pytest-monitor collects and aggregate data.

    :FUNCTION: Metrics collected for a single test function
    :MODULE: Metrics collected at module level
    :PACKAGE: Metrics collected at package level (not working yet)
    """
    FUNCTION = 'function'
    MODULE = 'module'
    PACKAGE = 'package'


class ResourceType(enum.Enum):
    """The different types of probed resources.

    :TOTAL_TIME: Real elapsed time
    :USER_TIME: Time spent running in user mode.
    :KERNEL_TIME: Time spent running in kernel mode.
    :CPU: Amount of CPU used
    :MEMORY: Amount of memory used
    """
    TOTAL_TIME = "total_time"
    USER_TIME = "user_time"
    KERNEL_TIME = "kernel_time"
    CPU = "cpu_usage"
    MEMORY = "mem_usage"


class ResourceMethod(enum.IntEnum):
    """Represents a sorting method.

    :LOWEST: sort in ascending order
    :TOP: sort in descending order
    """
    LOWEST = 0
    TOP = 1


class Field(enum.Enum):
    """Fields that can be used to control collections export.

    :SESSION_H: Session identifier
    :CONTEXT_H: Context identifier
    :ITEM_START_TIME: UTC Time at which the item has been run
    :ITEM_PATH: Python path like to the item
    :ITEM: Test identifier
    :ITEM_VARIANT: Fully qualified test identifier
    :ITEM_FS_LOC: Path to the python file hosting the test item.
    :KIND: Test scope
    :COMPONENT: Component or project to which the test belong.
    :TOTAL_TIME: Total time spent running the test
    :USER_TIME: Time spent in user mode while running the test.
    :KERNEL_TIME: Time spent in kernel mode while running the test
    :CPU_USAGE: Cpu usage while running the test.
    :MEM_USAGE: Memory usage of the test.
    :H: Session/Context identifier.
    :SCM: Source Code Management reference
    :RUN_DATE: Session start date
    :TAGS: Session description tags
    :CPU_COUNT: Number of CPU
    :CPU_FREQUENCY_MHZ: Max frequency of CPUs
    :CPU_TYPE: Cpu types (x64, ...)
    :CPU_VENDOR: CPU Vendor
    :RAM_TOTAL_MB: Amount of RAM on the machine
    :MACHINE_NODE: Fully qualified domain name
    :MACHINE_TYPE: Machine type
    :MACHINE_ARCH: Machine architecture
    :SYSTEM_INFO: Basic information about the kernel.
    :PYTHON_INFO: Basic information about the interpreter.
    """
    SESSION_H = 'session_h'
    CONTEXT_H = 'context_h'
    ITEM_START_TIME = 'start_time'
    ITEM_PATH = 'item_path'
    ITEM = 'item'
    ITEM_VARIANT = 'variant'
    ITEM_FS_LOC = 'path'
    KIND = 'kind'
    COMPONENT = 'component'
    TOTAL_TIME = 'wall_time'
    USER_TIME = 'user_time'
    KERNEL_TIME = 'kernel_time'
    CPU_USAGE = 'cpu_usage'
    MEM_USAGE = 'memory_usage'
    H = 'h'
    SCM = 'scm'
    RUN_DATE = 'run_date'
    TAGS = 'tags'
    CPU_COUNT = 'cpu_count'
    CPU_FREQUENCY_MHZ = 'cpu_freq'
    CPU_TYPE = 'cpu_type'
    CPU_VENDOR = 'cpu_vendor'
    RAM_TOTAL_MB = 'ram'
    MACHINE_NODE = 'hostname'
    MACHINE_TYPE = 'type'
    MACHINE_ARCH = 'arch'
    SYSTEM_INFO = 'sys'
    PYTHON_INFO = 'py'


METRIC_ALL_FIELDS = [Field.CONTEXT_H, Field.SESSION_H, Field.ITEM_START_TIME,
                     Field.ITEM_PATH, Field.ITEM, Field.ITEM_FS_LOC,
                     Field.ITEM_VARIANT, Field.KIND, Field.TOTAL_TIME,
                     Field.USER_TIME, Field.KERNEL_TIME, Field.CPU_USAGE,
                     Field.MEM_USAGE, Field.COMPONENT]


SESSION_ALL_FIELDS = [Field.SESSION_H, Field.SCM, Field.RUN_DATE, Field.TAGS]


CONTEXT_ALL_FIELDS = [Field.CONTEXT_H, Field.CPU_COUNT, Field.CPU_FREQUENCY_MHZ,
                      Field.CPU_TYPE, Field.CPU_VENDOR, Field.RAM_TOTAL_MB,
                      Field.MACHINE_NODE, Field.MACHINE_TYPE, Field.MACHINE_ARCH,
                      Field.SYSTEM_INFO, Field.PYTHON_INFO]
