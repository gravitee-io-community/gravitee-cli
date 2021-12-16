"""Packaging settings."""
import os
import sys
from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup
from setuptools.command.test import test as TestCommand

from graviteeio_cli.__version__ import __version__

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
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


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def get_install_requires():
    res = []
    res.append('click>=7.0,<8.1')
    res.append('configparser==3.8.1')
    res.append('requests>=2.22.0')
    res.append('click-completion>=0.5.2')
    res.append('terminaltables>=3.1.0')
    res.append('pyyaml>=5.1.2')
    res.append('jinja2>=2.10.1')
    res.append('dictdiffer>=0.8.0')
    res.append('jmespath>=0.10.0')
    res.append('asyncio==3.4.3')
    res.append('pytimeparse==1.1.8')
    res.append('termgraph==0.2.1')
    res.append('jsonschema==3.2.0')
    res.append('jsonpath-ng==1.5.2')

    return res


def get_packages_exclude():
    res = []
    res.append('docs')
    res.append('test')
    res.append('dist')
    res.append('build')
    res.append('doc-gen')

    return res


try:
    from cx_Freeze import setup, Executable

    base = 'Console'

    icon = None
    if os.path.exists('Graviteeio.ico'):
        icon = 'Graviteeio.ico'

    graviteeio_exe = Executable(
        "run_graviteeio.py",
        base=base,
        targetName="gio"
    )

    buildOptions = dict(packages=["asyncio", "ctypes", "appdirs", "packaging", "graviteeio_cli.commands.apim.apis"], excludes=["unittest"], includes=["idna.idnadata"])

    if sys.platform == "win32":
        graviteeio_exe = Executable(
            "run_graviteeio.py",
            base=base,
            targetName="gio.exe",
            icon=icon
        )

    setup(
        name='graviteeio-cli',
        version=__version__,
        description='Command line Client program in Python for graviteeio platform',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/gravitee-io/graviteeio-cli',
        author='Guillaume Gillon',
        author_email='guillaume.gillon@outlook.com',
        license='Apache License Version 2.0',
        classifiers=[
            'Intended Audience :: Developers',
            'Topic :: Utilities',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9'
        ],
        keywords=["Graviteeio", "gio", "gravitee", "configuration", "cli"],
        # packages = ["graviteeio_cli"],
        packages=find_packages(exclude=get_packages_exclude()),
        # packages = find_packages(exclude=['docs', 'tests*']),
        install_requires=get_install_requires(),
        extras_require={
            'test': ['coverage', 'pytest', 'pytest-cov'],
        },
        include_package_data=True,
        package_data={
            'graviteeio_cli': [
                'lint/rulesets/oas/schemas/*.json',
                'lint/rulesets/oas/schemas/ext_gravitee/*.json',
                'lint/rulesets/gio_apim/schemas/*.json'
            ]
        },
        entry_points={
            'console_scripts': [
                'gio = graviteeio_cli.cli:main',
            ],
        },
        options={'build_exe': buildOptions},
        executables=[graviteeio_exe]
    )


except ImportError:

    setup(
        name='graviteeio-cli',
        version=__version__,
        description='Command line Client program in Python for graviteeio platform',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/gravitee-io/graviteeio-cli',
        author='Guillaume Gillon',
        author_email='guillaume.gillon@outlook.com',
        license='Apache License Version 2.0',
        classifiers=[
            'Intended Audience :: Developers',
            'Topic :: Utilities',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9'
        ],
        keywords=["Graviteeio", "gio", "gravitee", "configuration", "cli"],
        # packages=["graviteeio_cli"],
        packages=find_packages(exclude=get_packages_exclude()),
        install_requires=get_install_requires(),
        extras_require={
            'test': ['coverage', 'pytest', 'pytest-cov'],
        },
        entry_points={
            'console_scripts': [
                'gio=graviteeio_cli.cli:main',
            ],
        },
        nclude_package_data=True,
        package_data={
            'graviteeio_cli': [
                'lint/rulesets/oas/schemas/*.json',
                'lint/rulesets/oas/schemas/ext_gravitee/*.json',
                'lint/rulesets/gio_apim/schemas/*.json'
            ]
        },
        cmdclass={'test': PyTest},
    )
