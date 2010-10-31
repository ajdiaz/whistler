#!/usr/bin/env python

from setuptools import setup, find_packages

NOSY_VERSION="1.0"

setup(
    name = "whistler",
    version = NOSY_VERSION,
    description = "A MUC bot for XMPP which handled commands.",
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
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Software Development',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Clustering',
          'Topic :: System :: Software Distribution',
          'Topic :: System :: Systems Administration',
    ],
)
