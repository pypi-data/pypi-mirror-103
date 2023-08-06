# -*- coding:utf-8 -*-
#!/usr/bin/env python

import os

import setuptools

with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="expyhist_crawler",
    version="0.0.1",
    description="simply web crawler",
    author="Expyh",
    author_email="exceptionalyh@gmail.com",
    url = "https://github.com/expyhist/expyhist_crawler",
    packages = setuptools.find_packages(exclude=("tests", "tests.*")),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "pandas",
        "random_user_agent",
    ],
    package_data = {"src": ["db/*.db","file/*"]}
)

