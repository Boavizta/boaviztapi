<p align="center">
    <img src="https://github.com/Boavizta/boaviztapi/blob/af7ca450518a2108f907736222a540908a258368/boavizta-logo-4.png" width="100">
</p>
<h1 align="center">
  Boavizta API
</h1>

An API to access [Boavizta's](https://boavizta.cmakers.io/) methodologies and impacts data [reference data](https://github.com/Boavizta/environmental-footprint-data).

See the [documentation](https://doc.api.boavizta.org/) for API usage and methodology.

[![Python tests](https://github.com/Boavizta/boaviztapi/actions/workflows/test.yml/badge.svg)](https://github.com/Boavizta/boaviztapi/actions/workflows/test.yml)

💬 [Join us on our public chat](https://chat.boavizta.org/signup_user_complete/?id=97a1cpe35by49jdc66ej7ktrjc)

## :dart: Objective

Boavizta aims to enhance the assessment of environmental impacts induced by ICTs in organizations by providing widespread access to our work in an automated and efficient manner.

Boavizta integrates various data and methodologies, which are combined and made accessible through this API.

Transparency and the popularization of scientific knowledge are of utmost importance in this project, and key aspects include open-sourcing the code, versioning the impact factors, and thoroughly documenting the project.

In the interest of transparency and scientific popularization, the opening of the code, the versioning of the impact factors and the documentation of the project are critical points. 

The system follows a bottom-up approach in its development, organized into layers. The initial layer focuses on equipment. The second layer focues on the impacts of digital services (e.g. cloud instances) or systems. However, assessing the overall global impact of ICT is currently beyond the project's scope.

## :fast_forward: Test it yourself (no installation)

* See our pedagogical front-end app (using the API) : <https://datavizta.boavizta.org/serversimpact>

* See the OpenAPI specification: <https://api.boavizta.org/docs>

* [Documentation](https://doc.api.boavizta.org/)

* Access the demo API: <https://api.boavizta.org>

## Run a local instance

## :whale: Run API using docker

```bash
$ docker run -p 5000:5000 ghcr.io/boavizta/boaviztapi:latest
```

Access API at http://localhost:5000

## Install using pip package

```bash
$ pip3 install boaviztapi
```

Then you can run the server locally with :

```bash
$ uvicorn boaviztapi.main:app --host=localhost --port 5000
```

## :computer: Development

### Prerequisite

Python 3, poetry recommended

### Setup poetry

Install poetry.

```bash
$ pip3 install poetry
```

Install dependencies and create a python virtual environment.

```bash
$ make install
$ poetry shell
```

### Launch a development server

**Once in the poetry environment**

Development server uses [uvicorn](https://www.uvicorn.org/) and [fastapi](https://fastapi.tiangolo.com/), you can launch development server with the `uvicorn` CLI.

```bash
$ uvicorn boaviztapi.main:app --host=localhost --port 5000
```

You can run the tests with `pytest`.

### Create your own docker image and run it

Build application package

```sh
make install
```

Build docker image

```sh
# using the makefile (recommended)
make docker-build

# manual build (requires to set version)
docker build --build-arg VERSION=`poetry version -s` .
```

Run docker image

```sh
docker run -p 5000:5000/tcp boavizta/boaviztapi:latest
```

### Deploy to AWS as serverless application

⚠ This is currently not working , see  [Deployment as serverless application does not work · Issue #153 · Boavizta/boaviztapi](https://github.com/Boavizta/boaviztapi/issues/153)

Api can be self hosted to your own AWS account using the serverless framework.

```sh
# Install the serverless framework and plugins
npm install -g serverless
npm i
# Authenticate
export AWS_PROFILE=your-own-profile
# Deploy to dev
serverless deploy
```

_Fisrt packaging/deployment may takes a several minutes_

### OpenAPI specification (Swagger)

Once API server is launched API swagger is available at [httsp://localhost:5000/docs](https://localhost:5000/docs).


## :woman: Contributing

See [contributing.md](./CONTRIBUTING.md)

You can build a source distribution (installable with pip) with `make build`.

## :one: Versioning

We use [Semantic Versioning 2.0.0](https://semver.org/)

|    Type     | Description                                                          |    Command        |
| :---        |    :----:                                                            |              ---: |
| MAJOR       | version when you make incompatible API changes                       | ```make major```  |
| MINOR       | version when you add functionality in a backwards compatible manner  | ```make minor```  |
| PATCH       | version when you make backwards compatible bug fixes                 | ```make patch```  |

## :two: Publishing

You can run : 

```shell
API_TOKEN=<your_token> make distribute 
```

## :scroll: License

GNU Affero General Public License v3.0
