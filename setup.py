#!/usr/bin/env python

from setuptools import setup


setup(
    name="reskeeper",
    version="0.1.1",
    url="https://github.com/qige96/reskeeper",
    license="MIT",
    description="A lightweight management system for applying and releasing exclusive resources.",
    long_description=open("README.md", "r", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    author="Ruiqi Zhu",
    author_email="rickyzhu@foxmail.com",
    package="reskeeper",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)