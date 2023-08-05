# -*- coding: utf-8 -*-
import os
import sys
from codecs import open
import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='guigebacktest',
    version='0.0.4',
    packages=setuptools.find_packages(),
    url='',
    license='MIT',
    author='guige',
    author_email='pangtongqing@guigeinvest.com',
    description='a backtest system',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires= [
        'matplotlib>=3.4.1',
        'pandas>=1.2.4',
        'empyrical>=0.3'
        'numpy>=1.20.2'
    ],
    package_data={
        # If any package contains *.yml ..files, include them:
        '': ['*.yml', '*.ini','*.xlsx', '*.xls', '*.md', '*.rst', '*.txt'],
        # And include any *.xml files found in the 'objMap' package, too:
        'objMap': ['*.xml'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
