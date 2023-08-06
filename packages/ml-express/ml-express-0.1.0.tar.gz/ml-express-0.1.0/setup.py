#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import ml_express

# def calculate_version():
#     initpy = open("ml-express/_version.py").read().split("\n")
#     version = list(filter(lambda x: "__version__" in x, initpy))[0].split("'")[1]
#     return version
with open("README.md", 'r') as f:
    long_description = f.read()

package_version = ml_express.__version__
setup(
    name="ml-express",
    version=package_version,
    author="Ved",
    author_email="vpved93@gmail.com",
    packages=find_packages(),
    url="https://github.com/ved93/ml-express",
    license="License :: OSI Approved :: MIT License",
    entry_points={"console_scripts": ["datacleaner=datacleaner:main"]},
    description=("A Python library for day to day data analysis and machine learning."),
    long_description= long_description
)