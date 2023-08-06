import os
import sys

from setuptools import setup

version = '1.0.5'

long_description = open('README.md').read()

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='ulog2kml',
    version=version,
    author='Casey Slaught',
    description='A command line program for converting ULog files into time-aware KML files.',
    keywords='ulog kml drone',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/caseyslaught/ulog2kml',
    packages=['ulog2kml'],
    python_requires=">=3.5",
    install_requires=[
        'numpy>=1.19.5',
        'simplekml>=1.3.5'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    scripts=['bin/ulog_to_kml.py'],
    entry_points = {
        'console_scripts': [
            'ulog_to_kml=bin.ulog_to_kml:main',
        ],
    },
)
