#!/usr/bin/env python
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='foxhole_sheets',
      version='1.11',
      description='Foxhole Stockpile Parsing',
      long_description=README,
      long_description_content_type="text/markdown",
      author="miles-igd",
      license="MIT",
      install_requires=[
      'opencv-python'
      ],
      packages=['sheets']
     )