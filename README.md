# monitor-server-api

[![CircleCI](https://circleci.com/gh/CFMTech/monitor-server-api.svg?style=svg)](https://circleci.com/gh/CFMTech/monitor-server-api)
![License](https://img.shields.io/badge/License-MIT-Blue.svg)
[![Documentation Status](https://readthedocs.org/projects/monitor-server-api/badge/?version=latest)](https://monitor-server-api.readthedocs.io/en/latest/?badge=latest)

## Features

For short, monitor-server-api helps you to collect, historicize and exploit the data from your tests
written with pytest and monitored with pytest-monitor.

* Centralize your tests results
    * bring support for *pytest-xdist* and *pytest-parallel*
* Easy data querying through specific queries
* Integrated library for in-script queries

## Usage

The server can be launched easily with any WSGI Framework.
The following lines can be used for a start:

```bash
bash $> # Use it with sqlite (not recomended for production)
bash $> export DATABASE_PATH=/path/to/sqlite/db
bash $> uwsgi --http 0.0.0.0:8050 --workers 8 --process 8 --master 
--harakiri 60 --harakiri-verbose --need-app -w monitor_server_api.uwsgi 
--callable WSGI_SERVER --env DATABASE_PATH=${DATABASE_PATH} --env ENV=prod
```

If you prefer using conda
```bash
bash $> conda activate <your monitor-server-api env>
bash $> launch-monitor-server.sh -p 8080 -t 60 -w 8 -u sqlite:////path/to/db
```

You can validate that the server runs correctly by going to the root page of the server.

## Documentation

> A full documentation with use cases and example is [available](https://link.to.readthedocs.org).

## Installation
Review the following installation instructions along with basic setup instructions.

You can install *monitor-server-api* via *conda* (through the `conda-forge` channel):

    $ conda install monitor-server-api -c https://conda.anaconda.org/conda-forge

 Another possibility is to install *monitor-server-api* via `pip`_ from `PyPI`:

    $ pip install monitor-server-api

## Requirements

### Monitor-Server-Api

To run, the monitor-server-api requires a valid Python 3.6+ interpreter. The following requirements
are needed:

* *flask-restx* (officially supported) OR *flask-restplus* (tested)
* *flask-sqlalchemy*

Testing requires *pytest-flask* and *pytest-cov* (along with *pytest* obviously).

### Monitorlib

The monitorlib also requires a valid Python 3.6+ along with :

* requests
* pandas

## Contributing

Contributions are very welcome. Tests are run with *[pytest](https://docs.pytest.org/en/latest/)*.
Before submitting a pull request, please ensure that:

- both internal tests and examples are passing.
- internal tests have been written if necessary.
- if your contribution provides a new feature, make sure to provide an
  example and update the documentation accordingly.

### Issues

If you encounter any problem, please file an issue along with a detailed
description.

See [contributing file](CONTRIBUTING.md) for more information.

## License

*monitor-server-api* is free, open-source software
This code is distributed under the ![MIT](https://img.shields.io/badge/License-MIT-Blue.svg) license.

## Author

The main author of `monitor-server-api` is Jean-Sébastien Dieu, ]]who can be reached at dieu.jsebastien@yahoo.com.
See [AUTHORS file](AUTHORS) for more contributors.
