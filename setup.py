import os
import sys

from setuptools import find_packages, setup

if sys.version_info < (2, 7):
    raise NotImplementedError(
        """\n
##############################################################
# globus-cli does not support python versions older than 2.7 #
##############################################################"""
    )


# single source of truth for package version
version_ns = {}
with open(os.path.join("globus_cli", "version.py")) as f:
    exec(f.read(), version_ns)
version = version_ns["__version__"]

setup(
    name="globus-cli",
    version=version,
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "globus-sdk==1.8.0",
        "click>=7.0,<8.0",
        "jmespath==0.9.4",
        "configobj>=5.0.6,<6.0.0",
        "requests>=2.0.0,<3.0.0",
        "six>=1.10.0,<2.0.0",
        # cryptography has unusual versioning and compatibility rules:
        # https://cryptography.io/en/latest/api-stability/
        # we trust the two next major versions, per the Deprecation policy
        #
        # as new versions of cryptography are released, we may need to update
        # this requirement
        "cryptography>=1.8.1,<3.0.0",
    ],
    extras_require={
        # deprecated, but do not remove -- doing so would break installs which
        # are already using this extra
        "delegate-proxy": [],
        # the development extra is for CLI developers only
        "development": [
            # drive testing with tox
            "tox>=3.5.3,<4.0",
            # linting
            "flake8>=3.0,<4.0",
            "isort>=4.3,<5.0",
            # black requires py3.6+
            'black==19.3b0;python_version>="3.6"',
            # flake-bugbear requires py3.5+
            'flake8-bugbear==19.3.0;python_version>="3.5"',
            # testing
            "pytest<5",
            # mock on py2, py3.4 and py3.5
            # not just py2: py3 versions of mock don't all have the same
            # interface!
            'mock==2.0.0;python_version<"3.6"',
        ],
    },
    entry_points={"console_scripts": ["globus = globus_cli:main"]},
    # descriptive info, non-critical
    description="Globus CLI",
    long_description=open("README.rst").read(),
    author="Stephen Rosen",
    author_email="sirosen@globus.org",
    url="https://github.com/globus/globus-cli",
    keywords=["globus", "cli", "command line"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
