# Gravitee Command Line Client

![pythonversion](https://img.shields.io/badge/python-3.7-brightgreen.svg?logo=Python&style=for-the-badge)

A command line client for Api Mangement tool - [Gravitee.io](https://gravitee.io/)


## Installation

(not available yet)
Install via `pip <https://pypi.python.org/pypi/pip>`__:

Use pip to install the latest stable version:
`$ pip install gravitee`

Install via wheel
`$ python setup.py bdist_wheel`
`$ pip install dist/my-project.whl`

## Requirements

 * Python 3.7
 * no additional modules are required.

## Configuration
Gravitee-cli need to know the gravitee APIm host. The default values are congured for the host `https://demo.gravitee.io/`. You can set it with the command `gravitee config`


	$ gravitee config --help
	Usage: gravitee config [OPTIONS]

    Gravitee cli configuration

    Options:
        --user TEXT  authentication user
        --pwd TEXT   authentication password
        --url TEXT   Gravitee Rest Management Url
        --env TEXT   Config environement
        --load TEXT  Load an environement saved
        --help       Show this message and exit.

