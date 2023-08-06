#!/usr/bin/env python

import os.path
import re
import sys
from setuptools import setup
import setuptools
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    sys.exit()


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


description = 'checkDebug debugger \
line by line debugging\
'




version = "0.0.1"

setup(
    name="checkDebug-swordyrepo",
    description=description,
    version=version,
    author='swordyrepo',
    author_email='swordysbot@gmail.com',
    url="https://github.com/swordysrepo/checkDebug",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    classifiers=[

        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    license='MIT'
    )
