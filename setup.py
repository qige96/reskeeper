#!/usr/bin/env python

from setuptools import setup


def get_long_description(long_description_file):
    """
    Read long description from file.
    """
    with open(long_description_file, encoding="utf-8") as f:
        long_description = f.read()

    return long_description_file

setup(
    name="reskeeper",
    version=0.1,
    license="MIT",
    description="A lightweight management system for applying and releasing exclusive resources.",
    long_description=get_long_description("README.md"),
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