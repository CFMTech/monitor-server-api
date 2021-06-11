# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

from monitor_server import SERVER
from monitor_server.data.model import *
from monitor_server.api.entry_points import set_entry_points as set_api_entry_points


def prepare_app():
    set_api_entry_points(SERVER)
    SERVER.DB.create_all()
    return SERVER


def main():
    prepare_app().run()
