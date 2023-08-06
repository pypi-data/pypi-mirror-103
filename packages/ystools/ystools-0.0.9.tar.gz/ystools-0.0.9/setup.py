# !/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="ystools",
    version="0.0.9",
    url='https://github.com.cnpmjs.org/zzyyww/ys_tools.git',
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=['qiniu']
)
