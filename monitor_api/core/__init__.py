# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT
#
# import enum
#
#
# class MetricType(enum.Enum):
#     FUNCTION = 'function'
#     MODULE = 'module'
#     PACKAGE = 'package'
#
#
# class MetricField(enum.Enum):
#     SESSION_H = 'session_h'
#     CONTEXT_H = 'context_h'
#     ITEM_START_TIME = 'start_time'
#     ITEM_PATH = 'item_path'
#     ITEM = 'item'
#     ITEM_VARIANT = 'variant'
#     ITEM_FS_LOC = 'path'
#     KIND = 'kind'
#     COMPONENT = 'component'
#     TOTAL_TIME = 'wall_time'
#     USER_TIME = 'user_time'
#     KERNEL_TIME = 'kernel_time'
#     CPU_USAGE = 'cpu_usage'
#     MEM_USAGE = 'memory_usage'
#
#
# METRIC_ALL_FIELDS = [MetricField.CONTEXT_H, MetricField.SESSION_H, MetricField.ITEM_START_TIME,
#                      MetricField.ITEM_PATH, MetricField.ITEM, MetricField.ITEM_FS_LOC,
#                      MetricField.ITEM_VARIANT, MetricField.KIND, MetricField.TOTAL_TIME,
#                      MetricField.USER_TIME, MetricField.KERNEL_TIME, MetricField.CPU_USAGE,
#                      MetricField.MEM_USAGE, MetricField.COMPONENT]
#
#
# class SessionField(enum.Enum):
#     H = 'h'
#     SCM = 'scm'
#     RUN_DATE = 'run_date'
#     TAGS = 'tags'
#
#
# SESSION_ALL_FIELDS = [SessionField.H, SessionField.SCM, SessionField.RUN_DATE, SessionField.TAGS]
#
#
# class ContextField(enum.Enum):
#     H = 'h'
#     CPU_COUNT = 'cpu_count'
#     CPU_FREQUENCY_MHZ = 'cpu_freq'
#     CPU_TYPE = 'cpu_type'
#     CPU_VENDOR = 'cpu_vendor'
#     RAM_TOTAL_MB = 'ram'
#     MACHINE_NODE = 'hostname'
#     MACHINE_TYPE = 'type'
#     MACHINE_ARCH = 'arch'
#     SYSTEM_INFO = 'sys'
#     PYTHON_INFO = 'py'
#
#
# CONTEXT_ALL_FIELDS = [ContextField.H, ContextField.CPU_COUNT, ContextField.CPU_FREQUENCY_MHZ,
#                       ContextField.CPU_TYPE, ContextField.CPU_VENDOR, ContextField.RAM_TOTAL_MB,
#                       ContextField.MACHINE_NODE, ContextField.MACHINE_TYPE, ContextField.MACHINE_ARCH,
#                       ContextField.SYSTEM_INFO, ContextField.PYTHON_INFO]
