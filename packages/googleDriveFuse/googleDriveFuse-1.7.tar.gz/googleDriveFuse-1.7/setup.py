#!/usr/bin/env python

import os
import setuptools

import googleDriveFuse

_APP_PATH = os.path.dirname(googleDriveFuse.__file__)

with open(os.path.join(_APP_PATH, 'resources', 'README.rst')) as f:
      long_description = f.read()

with open(os.path.join(_APP_PATH, 'resources', 'requirements.txt')) as f:
      install_requires = [s.strip() for s in f.readlines()]

setuptools.setup(
    name='googleDriveFuse',
    version=googleDriveFuse.__version__,
    description="Mount Google Drive onto linus system",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Topic :: System :: Filesystems',
        'Environment :: Console',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Utilities'
    ],
    keywords='google-drive google drive fuse filesystem',
    author='Jovi Vongnaraj',
    author_email='joviv172001@gmail.com',
    url='https://github.com/JoviVon/googleDriveFuse',
    packages=setuptools.find_packages(exclude=['tests']),
    include_package_data=True,
    package_data={
        'googleDriveFuse': [
            'resources/README.rst',
            'resources/requirements.txt'
        ],
    },
    zip_safe=False,
    install_requires=install_requires,
    scripts=[
        'googleDriveFuse/resources/scripts/gdfs',
        'googleDriveFuse/resources/scripts/gdfstool',
        'googleDriveFuse/resources/scripts/gdfsdumpentry',
    ],
)
