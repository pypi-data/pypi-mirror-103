#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

def readme():
    with open("README.txt") as f:
        readme = f.read()
    return readme

classifiers = [
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 3",
    ]

setup(
    name = "seadiver",
    version = "0.0.2",
    author = "KJ Chung",
    author_email = "kjchung495@yonsei.ac.kr",
    description = "DeepLearning Model Builder",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    license = "Apache Software License 2.0",
    keywords = "ANN, Artifictial Neural Network, DeepLearning",
    url = "https://github.com/kjchung495/seadiver",
    classifiers = classifiers,
    packages = ["seadiver"],
    include_package_data = True,
    install_requires = ['numpy']
)

