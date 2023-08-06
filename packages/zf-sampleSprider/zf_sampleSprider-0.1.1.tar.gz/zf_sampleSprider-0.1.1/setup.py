#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='zf_sampleSprider',
    version='0.1.1',
    author='zhangfan',
    author_email='1054934500@qq.com',
    url='https://github.com/ilovepythonJAVAc/test2020_8_4',
    description='简易爬虫',
    packages=['sampleSprider','sampleSprider.Common'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'fiction=sampleSprider.SampleSprider3_Fiction:main',
            'comics=sampleSprider.SampleSprider4_Comics1:main'
        ]
    }
)