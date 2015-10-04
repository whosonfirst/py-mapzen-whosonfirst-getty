#!/usr/bin/env python

from setuptools import setup, find_packages

packages = find_packages()
desc = open("README.md").read(),

setup(
    name='mapzen.whosonfirst.getty',
    namespace_packages=['mapzen', 'mapzen.whosonfirst', 'mapzen.whosonfirst.getty'],
    version='0.02',
    description='Python tools for working with Getty controlled vocabularies (and Who\'s On Firstdata)',
    author='Mapzen',
    url='https://github.com/mapzen/py-mapzen-whosonfirst-getty',
    install_requires=[
        'requests',
        'rdflib',
        'geojson',
        'atomicwrites',
        'mapzen.whosonfirst.geojson>=0.03',
        ],
    dependency_links=[
        'https://github.com/whosonfirst/py-mapzen-whosonfirst-geojson/tarball/master#egg=mapzen.whosonfirst.geojson-0.03',
        ],
    packages=packages,
    scripts=[
    ],
    download_url='https://github.com/mapzen/py-mapzen-whosonfirst-getty/releases/tag/v0.02',
    license='BSD')
