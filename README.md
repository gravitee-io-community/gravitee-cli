# Gravitee Command Line Client

![pythonversion](https://img.shields.io/badge/python-3-brightgreen.svg?logo=Python&style=for-the-badge)

A command line client for Api Mangement tool - [Gravitee.io](https://gravitee.io/)

`graviteeio-cli`is CLI (Command Line Interface). It helps you manage gravitee-io eco-system. It allow to automate the actions for all module of Gravitee Plateform.


## Installation

(not available yet)

Install via `pip <https://pypi.python.org/pypi/pip>`

Use pip to install the latest stable version:

`$ pip3 install graviteeio-cli`

Install via wheel:

`$ python setup.py bdist_wheel`

`$ pip3 install dist/graviteeio_cli-0.1.0-py3-none-any.whl`

## Requirements

 * Python 3.5 or more
 * no additional modules are required.

## Docker
Run Gravitee-cli with docker

Build:

`$ docker build -t gio .`

Run:

`$ docker run -v $(pwd):/graviteeio/conf gio apm apis ps`

## Get started

### API Management

#### Configuration
Graviteeio-cli need to know the gravitee API Management host. The default values are congured for the host `https://demo.gravitee.io/`. 

You can check the current configuration with the command:

`gio apim config get`

#### Display APIs

Display the list of available apis and their status

`gio apim apis ps`

#### Create API

We are going to see how create your first api

1. Initialization

"init" command will download in the local folder `graviteeio` the configuration template according to the version of the api management server

`gio apim apis init 1.30`

2. Value file

Now we need a value file that contains the API configuration values
You can dowload the follow: https://github.com/gravitee-io/graviteeio-cli/blob/master/examples/api_value.yml and place it in the folder `graviteeio`

3. Create the api

The only thing left to do is to execute the following command:

`gio apim apis create`

#### Create API

To update an API,  you just have to modify the file the `api_value.yml` file and execute the following command:

`gio apim apis update [API ID]`

*[API ID]: replace with ID of your API*


For more information, you can use `--help` on each module

## Usage

`gio <module> <command>`

module:
- apim: API Management
- am: Access Management

### apim

* [apim config](https://github.com/gravitee-io/graviteeio-cli/blob/master/docs/apim-config.md)
    * [apim config get](https://github.com/gravitee-io/graviteeio-cli/blob/master/docs/apim-config-get.md)
    * [apim config set](https://github.com/gravitee-io/graviteeio-cli/blob/master/docs/apim-config-set.md)
    * [apim config load](https://github.com/gravitee-io/graviteeio-cli/blob/master/docs/apim-config-load.md)

* apim apis
    * [apim apis ps](https://github.com/gravitee-io/graviteeio-cli/blob/master/docs/apim-apis-ps.md)
    * apim apis init
    * apim apis upgrade
    * apim apis create
    * apim apis update
    * apim apis start
    * apim apis stop
    * apim apis deploy




