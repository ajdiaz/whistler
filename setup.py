#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path

WHISTLER_VERSION="1.5.3"


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
    entry_points={
        'console_scripts': [
            'whistler = whistler.scripts:main'
        ]
    },
    install_requires = [
        "sleekxmpp>=1.0",
        "pyasn1>=0.1.4",
        "pyasn1-modules>=0.0.4",
        "twitter>=1.9.4",
        "bitly-api>=0.2",
    ],
    classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Communications :: Chat',
    ],
)
