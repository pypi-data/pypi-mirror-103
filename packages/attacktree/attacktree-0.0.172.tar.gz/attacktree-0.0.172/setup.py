import io
import os
import sys
from shutil import rmtree

from setuptools import setup, find_packages

#
# Based on
# https://github.com/navdeep-G/setup.py/blob/master/setup.py
# 

# Package meta-data.
NAME = 'attacktree'
DESCRIPTION = 'Describe attack-defense-attack sequences using python.'
URL = 'https://github.com/hyakuhei/attackTrees'
EMAIL = 'hyakuhei@gmail.com'
AUTHOR = 'hyakuhei'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = '0.0.172'

REQUIRED = [
    "graphviz >=0.16"
]

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    py_modules=['attacktree'],
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7'
    ]
)