#!/usr/bin/env python

try:
    from setuptools import setup
except:
    from distutils.core import setup

from os.path import join, dirname

package_info = open(join(dirname(__file__), 'tornalet_info.txt')).readlines()

setup(
    name = "tornalet",
    description = "Tornado + Greenlet = Beautiful",
    
    py_modules = ["tornalet"],
    install_requires = [
        "greenlet",
        "tornado",
    ],

    version = package_info[4],
    author = package_info[5],
    author_email = package_info[6],
    url = "https://github.com/Gawen/tornalet",
    license = package_info[3],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_data={'': ['tornalet_info.txt']},
    include_package_data=True
)
