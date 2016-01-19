#!/usr/bin/env python

# Remove .egg-info directory if it exists, to avoid dependency problems with
# partially-installed packages (20160119/dphiffer)

import os, sys
from shutil import rmtree

cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
egg_info = cwd + "/mapzen.whosonfirst.getty.egg-info"
if os.path.exists(egg_info):
    rmtree(egg_info)

from setuptools import setup, find_packages

packages = find_packages()
desc = open("README.md").read()
desc = open("VERSION").read()

setup(
    name='mapzen.whosonfirst.getty',
    namespace_packages=['mapzen', 'mapzen.whosonfirst', 'mapzen.whosonfirst.getty'],
    version=version,
    description='Python tools for working with Getty controlled vocabularies (and Who\'s On First data)',
    author='Mapzen',
    url='https://github.com/whosonfirst/py-mapzen-whosonfirst-getty',
    install_requires=[
        'requests',
        'rdflib',
        'geojson',
        'atomicwrites',
        'mapzen.whosonfirst.geojson>=0.06',
        ],
    dependency_links=[
        'https://github.com/whosonfirst/py-mapzen-whosonfirst-geojson/tarball/master#egg=mapzen.whosonfirst.geojson-0.06',
        ],
    packages=packages,
    scripts=[
    ],
    download_url='https://github.com/whosonfirst/py-mapzen-whosonfirst-getty/releases/tag/' + version,
    license='BSD')
