#!/usr/bin/env python

from setuptools import setup, find_packages

packages = find_packages()
desc = open("README.md").read(),

setup(
    name='mapzen.whosonfirst.getty',
    namespace_packages=['mapzen', 'mapzen.whosonfirst', 'mapzen.whosonfirst.getty'],
    version='0.01',
    description='Python tools for working with Getty controlled vocabularies (and Who\'s On Firstdata)',
    author='Mapzen',
    url='https://github.com/mapzen/py-mapzen-whosonfirst-getty',
    install_requires=[
        'requests',
        'rdflib',
        ],
    dependency_links=[
        ],
    packages=packages,
    scripts=[
    ],
    download_url='https://github.com/mapzen/py-mapzen-whosonfirst-getty/releases/tag/v0.01',
    license='BSD')
