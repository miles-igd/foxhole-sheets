#!/usr/bin/env python
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='foxhole-sheets',
      version='2.0.1',
      description='Foxhole Stockpile Parsing',
      long_description=README,
      long_description_content_type="text/markdown",
      url="https://github.com/miles-igd/foxhole-sheets",
      author="miles-igd",
      license="MIT",
      include_package_data=True,
      install_requires=[
      'opencv-python'
      ],
      packages=['sheets']
     )