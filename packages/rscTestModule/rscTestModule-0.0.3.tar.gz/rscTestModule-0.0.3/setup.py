#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 13:21:55 2021

@author: rohitchauhan
"""

from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name = 'rscTestModule',
    version = '0.0.3',
    description = 'first package for testing purpose',
    long_description = open('README.txt').read(),
    url = '',
    author = 'Rohit Singh Chuahan',
    author_email = 'rsc.iitkgp@gmail.com',
    license = 'MIT',
    classifiers = classifiers, 
    keywords = 'calculator',
    packages = find_packages(),
)
