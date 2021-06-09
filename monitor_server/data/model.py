# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from monitor_server import SERVER

if SERVER.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:'):
    from sqlalchemy.dialects.sqlite.json import JSON
else:
    from sqlalchemy.dialects.postgresql.json import JSON


class MetricModel(SERVER.DB.Model):
    __tablename__ = 'TEST_METRICS'

    test_id = SERVER.DB.Column('ITEM_PK', SERVER.DB.Integer, primary_key=True)
    session_h = SERVER.DB.Column('SESSION_H', SERVER.DB.ForeignKey('TEST_SESSIONS.SESSION_H'))
    ctx_h = SERVER.DB.Column('CONTEXT_H', SERVER.DB.ForeignKey('EXECUTION_CONTEXTS.ENV_H'))
    item_start_time = SERVER.DB.Column('ITEM_START_TIME', SERVER.DB.String(64), nullable=False)
    item_path = SERVER.DB.Column('ITEM_PATH', SERVER.DB.String(4096), nullable=False)
    item = SERVER.DB.Column('ITEM', SERVER.DB.String(2048), nullable=False)
    item_variant = SERVER.DB.Column('ITEM_VARIANT', SERVER.DB.String(2048), nullable=False)
    item_fs_loc = SERVER.DB.Column('ITEM_FS_LOC', SERVER.DB.String(2048), nullable=False)
    kind = SERVER.DB.Column('KIND', SERVER.DB.String(64), nullable=False)
    component = SERVER.DB.Column('COMPONENT', SERVER.DB.String(512), nullable=True)
    wall_time = SERVER.DB.Column('TOTAL_TIME', SERVER.DB.Float, nullable=False)
    user_time = SERVER.DB.Column('USER_TIME', SERVER.DB.Float, nullable=False)
    krnl_time = SERVER.DB.Column('KERNEL_TIME', SERVER.DB.Float, nullable=False)
    cpu_usage = SERVER.DB.Column('CPU_USAGE', SERVER.DB.Float, nullable=False)
    mem_usage = SERVER.DB.Column('MEM_USAGE', SERVER.DB.Float, nullable=False)


class ExecutionContextModel(SERVER.DB.Model):
    __tablename__ = 'EXECUTION_CONTEXTS'

    h = SERVER.DB.Column('ENV_H', SERVER.DB.String(64), primary_key=True, nullable=False)
    cpu_count = SERVER.DB.Column('CPU_COUNT', SERVER.DB.Integer, nullable=False)
    cpu_freq = SERVER.DB.Column('CPU_FREQUENCY_MHZ', SERVER.DB.Integer, nullable=False)
    cpu_type = SERVER.DB.Column('CPU_TYPE', SERVER.DB.String(64), nullable=False)
    cpu_vendor = SERVER.DB.Column('CPU_VENDOR', SERVER.DB.String(256), nullable=True)
    ram_total = SERVER.DB.Column('RAM_TOTAL_MB', SERVER.DB.Integer, nullable=False)
    mac_node = SERVER.DB.Column('MACHINE_NODE', SERVER.DB.String(512), nullable=False)
    mac_type = SERVER.DB.Column('MACHINE_TYPE', SERVER.DB.String(32), nullable=False)
    mac_arch = SERVER.DB.Column('MACHINE_ARCH', SERVER.DB.String(16), nullable=False)
    sys_info = SERVER.DB.Column('SYSTEM_INFO', SERVER.DB.String(256), nullable=False)
    py_info = SERVER.DB.Column('PYTHON_INFO', SERVER.DB.String(512), nullable=False)
    ctx_h_rel = SERVER.DB.relationship('MetricModel', backref='exec_ctx', lazy=True)


class SessionModel(SERVER.DB.Model):
    __tablename__ = 'TEST_SESSIONS'

    h = SERVER.DB.Column('SESSION_H', SERVER.DB.String(64), primary_key=True, nullable=False)
    run_date = SERVER.DB.Column('RUN_DATE', SERVER.DB.String(64), nullable=False)
    scm_ref = SERVER.DB.Column('SCM_REF', SERVER.DB.String(128), nullable=True)
    description = SERVER.DB.Column('DESCRIPTION', SERVER.DB.JSON(), nullable=True)
    session_h_rel = SERVER.DB.relationship('MetricModel', backref='sessions_ctx', lazy=True)
