"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

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
        'License :: Apache License Version 2.0',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = ["Swagger", "OpenAPI", "Graviteeio"],
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['click', 'configparser', 'requests', 'click-completion', 'terminaltables', 'pyyaml', 'jinja2'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'graviteeio=graviteeio_cli.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)
