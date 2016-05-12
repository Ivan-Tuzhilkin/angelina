#!/usr/bin/env python3

"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/Ivan-Tuzhilkin/angelina.git
"""

from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name = 'angelina',
    version = '1.0',
    description = 'The software for creating archives.',
    long_description = open(join(dirname(__file__), 'README.rst')).read(),
	# Author details
    author = 'Ivan Tuzhilkin',
    author_email = 'tiv57@hotmail.com',
	# Choose your license
    license = 'MIT',
	# The project's main homepage.
    url = 'https://github.com/Ivan-Tuzhilkin/angelina.git',
    packages = find_packages(),
    entry_points = {
        'console_scripts':
            ['angelina = angelina.main:startapp', 'angelina-test = angelina.tests:create_test_space']
        }
    )
