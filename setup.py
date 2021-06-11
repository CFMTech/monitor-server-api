#!/usr/bin/env python

# SPDX-FileCopyrightText: 2021 Jean-Sébastien Dieu <jean-sebastien.dieu@cfm.fr>
#
# SPDX-License-Identifier: MIT
import os
import pathlib
import re
from setuptools import setup, find_packages


def read_version():
    p = pathlib.Path(__file__)
    p = p.parent / "monitor_server" / '__init__.py'
    with p.open('r') as f:
        for line in f:
            if line.startswith('__version__'):
                line = line.split('=')[1].strip()
                match = re.match(r"^['\"](\d+\.\d+\.\d+\w*)['\"]", line)
                if match:
                    return match.group(1)
    raise ValueError('Unable to compute version')


def read(fname):
    file_path = pathlib.Path(__file__).parent / fname
    with file_path.open('r', encoding='utf-8') as f:
        return f.read()


def get_requirements():
    requirements = pathlib.Path(__file__).parent / 'requirements.txt'
    if not requirements.exists() and os.environ.get('RTD_CONTEXT', 'no') == 'yes':
        requirements = pathlib.Path(__file__).parent / 'requirements-prod.txt'

    with requirements.open('r', encoding='utf-8') as f:
        packages = f.readlines()
        packages.append('wheel')
    return list(set([i for i in packages])) 


setup(
    name='monitor-server-api',
    version=read_version(),
    author='Jean-Sébastien Dieu',
    author_email='dieu.jsebastien@yahoo.com',
    maintainer='Jean-Sébastien Dieu',
    maintainer_email='dieu.jsebastien@yahoo.com',
    license='MIT',
    project_urls=dict(Source='https://github.com/js-dieu/monitor-server-api',
                      Tracker='https://github.com/js-dieu/monitor-server-api/issues'),
    url='https://monitor-server-api.readthedocs.io/',
    description='A REST API that can be used a central point for collecting metrics from pytest-monitor.',
    entry_points={'console_scripts': ['monitor-server=monitor_server.app:main']},
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages('.', exclude=('tests', 'example', 'docs')),
    package_data={'monitor_server': ['templates/*']},
    include_package_data=True,
    python_requires='>=3.6',
    scripts=['scripts/launch-monitor-server.sh'],
    install_requires=get_requirements(),
    options={"bdist_wheel": {"universal": False}},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6', 
        'Programming Language :: Python :: 3.7', 
        'Programming Language :: Python :: 3.8', 
        'Programming Language :: Python :: 3.9', 
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
)
