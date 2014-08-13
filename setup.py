#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='Doner',
    version='0.0.1',
    author='Tomasz Karbownicki',
    author_email='tomasz@karbownicki.com',
    url='https://github.com/trojkat/doner',
    license='LICENSE.txt',
    description='Ticket Management System for Getting Things Done™ (TMS4GTD)',
    long_description=open('README.md').read(),
    packages=['doner'],
    install_requires=[
        "Django == 1.6.5",
    ],
)
