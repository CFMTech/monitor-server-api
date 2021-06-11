#!/bin/bash

# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT

THIS_SCRIPT="${0##*/}"
NOW=$(date "+%Y%m%d_%H%M%S")

DEFAULT_PORT=8181
DEFAULT_TIMEOUT=60
DEFAULT_WORKERS=4
DEFAULT_ITEM_PER_PAGE=500
DEFAULT_LOGDIR=${TMPDIR:-$PWD}


die() {
  echo "$1" 1>&2
  exit 1
}

usage() {
  cat << EOF
Usage: ${THIS_SCRIPT} [-p PORT] [-t TIMEOUT] [-w WORKERS] [-c ITEM_PER_PAGE]
                      [-S] [-u DATABASE_URL] [-L LOGDIR] [-h]

Synopsys
This script aims at facilitating the launching of the monitor-server.

Options
  -p          PORT   Force monitor-server to run on the given PORT if
                     this later is available.
                     Default is ${DEFAULT_PORT}.

  -t       TIMEOUT   Aborts workers that are serving requests for an excessively long time.
                     Default is ${DEFAULT_TIMEOUT}s.

  -w       WORKERS   Spawn the specified number of workers.
                     Default is ${DEFAULT_WORKERS} processes.

  -c ITEM_PER_PAGE   Customize the pagination done by the server.
                     Default is ${DEFAULT_ITEM_PER_PAGE} item per page.

  -u  DATABASE_URL   URL to the database. Valid URI are:
                       - for sqlite: sqlite:///<path>
                       - for postgres: postgre:///<url>

  -L       LOGDIR    Path to where logs will be written.

  -S  CERTIFICATE    Enable HTTPS mode. Requires path to your certificate.
                     Use comma to chain certificates.

  -h  Show this help
EOF

  exit 1;
}


while getopts "h:S:p:t:w:c:u:L:" o; do
    case "${o}" in
        t)
            user_timeout=${OPTARG}
            ;;
        w)
            user_workers=${OPTARG}
            ;;
        c)
            user_item_per_page=${OPTARG}
            ;;
        u)
            user_db_url=${OPTARG}
            ;;
        p)
            user_port=${OPTARG}
            ;;
        L)
            user_logdir=${OPTARG}
            ;;
        S)
            user_certs=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))


[ -z "${user_db_url}" ] && die "A database must be set!"

port=${user_port:-${DEFAULT_PORT}}
timeout=${user_timeout:-${DEFAULT_TIMEOUT}}
workers=${user_workers:-${DEFAULT_WORKERS}}
item_per_page=${user_item_per_page:-${DEFAULT_ITEM_PER_PAGE}}
log_file=${user_logdir:-${DEFAULT_LOGDIR}}/uwsgi.${NOW}.log
pid_file=${user_logdir:-${DEFAULT_LOGDIR}}/uwsgi.${port}.pid

cat << EOF

  Your configuration
      PORT .......... ${port}
      TIMEOUT ....... ${timeout}
      WORKERS ....... ${workers}
      ITEM_PER_PAGE . ${item_per_page}
      DATABASE_URL .. ${user_db_url}
      LOGDIR ........ ${log_file}
      CERTIFICATE ... ${user_certs:-}
      PID FILE ...... ${pid_file}
EOF

if [ -z  "${certs:-}" ]; then
  exec nohup uwsgi --master --need-app -w monitor_server.uwsgi --callable WSGI_SERVER \
                   --die-on-term \
                   --http "0.0.0.0:${port}" --buffer-size=32768 \
                   --harakiri "${timeout}" --harakiri-verbose \
                   --workers "${workers}" \
                   --env FLASK_ENV=prod \
                   --env MONITOR_SERVER_DATABASE_URI="${user_db_url}"\
                   --env MONITOR_SERVER_PAGINATION_COUNT="${item_per_page}" \
                   --pidfile "${pid_file}" > "${log_file}" 2>&1 &
else
  exec nohup uwsgi --master --need-app -w monitor_server.uwsgi --callable WSGI_SERVER \
                   --die-on-term \
                   --https "0.0.0.0:${port},${certs}" --buffer-size=32768 \
                   --harakiri "${timeout}" --harakiri-verbose \
                   --workers "${workers}" \
                   --env FLASK_ENV=prod \
                   --env MONITOR_SERVER_DATABASE_URI="${user_db_url}" \
                   --env MONITOR_SERVER_PAGINATION_COUNT="${item_per_page}" \
                   --pidfile "${pid_file}" > "${log_file}" 2>&1 &
fi

sleep 1

pid=$(cat "${pid_file}")
if [ -d "/proc/${pid}" ]; then
  echo "Server is running. PID is ${pid}"
  exit 0
else
  echo "Unable to retrieve server's PID."
  exit 1
fi
