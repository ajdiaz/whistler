#!/usr/bin/env python

from setuptools import setup, find_packages

NOSY_VERSION="1.0"

setup(
    name = "whistler",
    version = NOSY_VERSION,
    description = "An extensible MUC bot for XMPP.",
    long_description=open('README.rst').read() + """
    For more information, point to whistler web.""",
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
