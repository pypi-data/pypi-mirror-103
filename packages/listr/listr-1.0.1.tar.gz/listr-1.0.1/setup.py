#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='listr',
    version='1.0.1',
    packages=['listr',],
    license='MIT',
    author="Slamet Hidayat",
    author_email="myawn@pm.me",
    description="python list with pointer",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="list pointer",
    url="https://fb.me/Slamet. HidayatCirebon",   
)