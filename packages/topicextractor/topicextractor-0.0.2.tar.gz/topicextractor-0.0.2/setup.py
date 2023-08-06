#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

def readme():
    with open("README.txt") as f:
        readme = f.read()
    return readme

classifiers = [
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ]

setup(
    name = "topicextractor",
    version = "0.0.2",
    author = "KJ Chung",
    author_email = "kjchung495@yonsei.ac.kr",
    description = "Extracts keywords with 'TF-IDF' algorithm",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    license = "Apache Software License 2.0",
    keywords = "TFIDF, topic analysis",
    url = "https://github.com/kjchung495/topicextractor",
    classifiers = classifiers,
    packages = ["topicextractor"],
    include_package_data = True,
    install_requires = []
)

