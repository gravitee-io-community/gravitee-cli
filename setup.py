"""Packaging settings."""
import os
import sys

from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from graviteeio_cli.__version__ import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.adoc'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=skele', '--cov-report=term-missing'])
        raise SystemExit(errno)

def get_install_requires():
    res = []
    res.append('urllib3>=1.24.2,<1.25')
    res.append('requests>=2.20.0')
    res.append('boto3>=1.9.142')
    res.append('requests_aws4auth>=0.9')
    res.append('click>=6.7,<=7.0')
    res.append('pyyaml==3.13')
    res.append('voluptuous>=0.9.3')
    res.append('certifi>=2019.6.16')
    res.append('six>=1.11.0')
    return res

try:
    from cx_Freeze import setup, Executable

    base = 'Console'

    icon = None
    if os.path.exists('Graviteeio.ico'):
        icon = 'Elastic.ico'

    graviteeio_exe = Executable (
        "run_graviteeio.py",
        base=base,
        targetName = "gio"
    )

    buildOptions = dict(packages=["asyncio","ctypes","appdirs", "packaging"], excludes=[], includes=["idna.idnadata"])

    if sys.platform == "win32":
        graviteeio_exe = Executable(
            "run_graviteeio.py",
            base=base,
            targetName = "gio.exe",
            icon = icon
        )

    setup(
        name = 'graviteeio-cli',
        version = __version__,
        description = 'Command line Client program in Python for graviteeio plateform',
        long_description = long_description,
        long_description_content_type="text/markdown",
        url = 'https://github.com/gravitee-io/graviteeio-cli',
        author = 'Guillaume Gillon',
        author_email = 'guillaume.gillon@outlook.com',
        license = 'Apache License Version 2.0',
        classifiers = [
            'Intended Audience :: Developers',
            'Topic :: Utilities',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7'
        ],
        keywords = ["Graviteeio", "gio", "gravitee","configuration", "cli"],
        packages = ["graviteeio_cli"],
        #packages = find_packages(exclude=['docs', 'tests*']),
        install_requires = [
            'click>=7.0,<8.0', 
            'configparser==3.8.1', 
            'requests>=2.22.0', 
            'click-completion>=0.5.1', 
            'terminaltables>=3.1.0', 
            'pyyaml>=5.1.2', 
            'jinja2>=2.10.1',
            'dictdiffer>=0.8.0',
            'jmespath>=0.9.4',
            'aiohttp==3.6.2'],
        extras_require = {
            'test': ['coverage', 'pytest', 'pytest-cov'],
        },
        include_package_data=True,
        entry_points = {
            'console_scripts': [
                'gio = graviteeio_cli.cli:main',
            ],
        },
        cmdclass = {'test': RunTests},
        options = {'build_exe' : buildOptions},
        executables = [graviteeio_exe]
    )



except ImportError:

    setup(
        name = 'graviteeio-cli',
        version = __version__,
        description = 'Command line Client program in Python for graviteeio plateform',
        long_description = long_description,
        long_description_content_type="text/markdown",
        url = 'https://github.com/gravitee-io/graviteeio-cli',
        author = 'Guillaume Gillon',
        author_email = 'guillaume.gillon@outlook.com',
        license = 'Apache License Version 2.0',
        classifiers = [
            'Intended Audience :: Developers',
            'Topic :: Utilities',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7'
        ],
        keywords = ["Graviteeio", "gio", "gravitee","configuration", "cli"],
        packages = ["graviteeio_cli"],
        #packages = find_packages(exclude=['docs', 'tests*']),
        install_requires = [
            'click>=7.0,<8.0', 
            'configparser==3.8.1', 
            'requests>=2.22.0', 
            'click-completion>=0.5.1', 
            'terminaltables>=3.1.0', 
            'pyyaml>=5.1.2', 
            'jinja2>=2.10.1',
            'dictdiffer>=0.8.0',
            'jmespath>=0.9.4',
            'aiohttp==3.6.2'],
        extras_require = {
            'test': ['coverage', 'pytest', 'pytest-cov'],
        },
        entry_points = {
            'console_scripts': [
                'gio = graviteeio_cli.cli:main',
            ],
        },
        cmdclass = {'test': RunTests},
    )
