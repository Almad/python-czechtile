#!/usr/bin/env python

"""Installs package using distutils

Run:
    python setup.py install

to install this package.
"""

try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup

from distutils.command.install import INSTALL_SCHEMES
import sys

required_python_version = '2.4'

###############################################################################
# arguments for the setup command
###############################################################################
import czechtile
name = "czechtile"
version = czechtile.__versionstr__[len(name)+1:]
desc = "Python implementation of Czechtile WikiSyntax"
long_desc = """Czechtile is WikiSyntax intended to be used on Czech keyboard layout: this is Python module for
handling Czechtile input and transformation into DocBook and XHTML."""
classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Natural Language :: Czech",
    "Topic :: Software Development :: Documentation",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Text Processing",
    "Topic :: Text Processing :: Markup :: HTML",
    "Topic :: Text Processing :: Markup :: XML"
]
author="Lukas Almad Linhart"
author_email="bugs@almad.net"
url="http://projects.almad.net/czechtile"
cp_license="BSD"
packages=[
    "czechtile",
    "czechtile.expanders",
]
download_url="http://www.almad.net/download/czechtile/"+czechtile.__versionstr__+".tar.gz"
data_files=[]
scripts = ['bin/czechtile']

###############################################################################
# end arguments for setup
###############################################################################

def main():
    if sys.version < required_python_version:
        s = "I'm sorry, but %s %s requires Python %s or later."
        print s % (name, version, required_python_version)
        sys.exit(1)

    # set default location for "data_files" to platform specific "site-packages"
    # location
    for scheme in INSTALL_SCHEMES.values():
        scheme['data'] = scheme['purelib']

    setup(
        name=name,
        scripts=scripts,
        version=version,
        description=desc,
        long_description=long_desc,
        classifiers=classifiers,
        author=author,
        author_email=author_email,
        url=url,
        license=cp_license,
        packages=packages,
        download_url=download_url,
        data_files=data_files,
    )

if __name__ == "__main__":
    main()
