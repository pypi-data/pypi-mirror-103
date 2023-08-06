#!/usr/bin/env python

from distutils.core import setup

setup(
    name='python-reddcoinrpc',
    version='1.1',
    description='Enhanced version of python-jsonrpc for use with Reddcoin',
    long_description=open('README.rst').read(),
    author='John Nash',
    author_email='<gnasher@reddcoin.com>',
    maintainer='John Nash',
    maintainer_email='<gnasher@reddcoin.com>',
    url='http://www.github.com/reddcoin-project/python-reddcoinrpc',
    packages=['reddcoinrpc'],
    classifiers=[
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)', 'Operating System :: OS Independent'
    ]
)
