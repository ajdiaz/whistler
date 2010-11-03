#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path

WHISTLER_VERSION="1.0"


def get_file_contents(filename):
    fd = file(path.join(path.dirname(__file__), filename), "r")
    content = fd.read()
    fd.close()
    return content

setup(
    name = "whistler",
    version = WHISTLER_VERSION,
    description = "An extensible MUC bot for XMPP.",
    long_description=get_file_contents("README.rst"),
    author='Andres J. Diaz',
    author_email='ajdiaz@connectical.com',
    url='http://github.com/ajdiaz/whistler',
    packages=find_packages(),
    install_requires=[ "xmpppy >= 0.5.0rc1" ],
    entry_points={
        'console_scripts': [
            'whistler = whistler.scripts:main'
        ]
    },
    classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Communications :: Chat',
    ],
)
