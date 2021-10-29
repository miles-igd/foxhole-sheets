#!/usr/bin/env python

from setuptools import setup

setup(name='foxhole_sheets',
      version='1.11',
      description='Foxhole Stockpile Analysis',
      install_requires=[
      'opencv-python'
      ],
      packages=['sheets']
     )