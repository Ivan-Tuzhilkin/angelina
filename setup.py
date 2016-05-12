#!/usr/bin/env python3
from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name = 'angelina',
    version = '1.0',
    description = 'The software for creating archives.',
    long_description = open(join(dirname(__file__), 'README.rst')).read(),
    author = 'Ivan Tuzhilkin',
    author_email = 'tiv57@hotmail.com',
    license = 'MIT',
    url = 'https://github.com/Ivan-Tuzhilkin/angelina.git',
    packages = find_packages(),
    entry_points = {
        'console_scripts':
            ['angelina = angelina.main:startapp', 'angelina-test = angelina.tests:create_test_space']
        }
    )
