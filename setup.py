#!/usr/bin/env python

try:
    from setuptools import setup
except:
    from distutils.core import setup

import tornalet_info

setup(
    name = "tornalet",
    description = "Tornado + Greenlet = Beautiful",

    py_modules=['tornalet_info', 'tornalet'],
    install_requires = [
        "greenlet",
        "tornado",
    ],

    version = tornalet_info.__version__,
    author = tornalet_info.__author__,
    author_email = tornalet_info.__email__,
    url = "https://github.com/Gawen/tornalet",
    license = tornalet_info.__license__,
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
