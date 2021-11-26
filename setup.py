#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ 
                'pandas>=1.0',
                'numpy>=1.0']

test_requirements = ['pytest>=3', ]

setup(
    author="Drew Heasman",
    author_email='heasman.drew@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A Python package for caclulations and visualizations in geological sciences.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='geo_calcs',
    name='geo_calcs',
    packages=find_packages(include=['geo_calcs', 'geo_calcs.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://git.cs.usask.ca/msv275/geo_calcs',
    version='0.1.3',
    zip_safe=False,
)
