#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='zf_sampleSprider',
    version='0.1.4',
    author='zhangfan',
    author_email='1054934500@qq.com',
    url='https://github.com/ilovepythonJAVAc/test2020_8_4',
    description='简易爬虫',
    packages=['sampleSprider','sampleSprider.Common'],
    install_requires=[
        'requests>=2.25.1',
        'beautifulsoup4>=4.9.3',
        'selenium>=3.141.0',
        'lxml>=4.6.3'
    ],
    entry_points={
        'console_scripts': [
            'fiction=sampleSprider.SampleSprider3_Fiction:main',
            'comics=sampleSprider.SampleSprider4_Comics1:main'
        ]
    }
)