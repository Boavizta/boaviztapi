<p align="center">
    <img src="https://github.com/Boavizta/boaviztapi/blob/main/boaviztapi_color.svg" height="100" alt="BoaviztAPI">
</p>

<h3 align="center">
   An API to access <a href="https://boavizta.cmakers.io/">Boavizta's</a> methodologies and data</a>
</h3>

---

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

* See our pedagogical front-end app (using the API): <https://datavizta.boavizta.org/serversimpact>

* See the OpenAPI specification: <https://api.boavizta.org/docs>

* [Documentation](https://doc.api.boavizta.org/)

* Access the demo API: <https://api.boavizta.org>

## Run a local instance

### :whale: Run API using docker

```bash
$ docker run -p 5000:5000 ghcr.io/boavizta/boaviztapi:latest
```

Access the API at http://localhost:5000.

### Install using pip package

```bash
$ pip3 install boaviztapi
```

Run the server locally with:

```bash
$ uvicorn boaviztapi.main:app --host=localhost --port 5000
```

## :computer: Development

### Prerequisite

- Python >=3.12
- [Poetry](https://python-poetry.org/) (see the [install instructions](https://python-poetry.org/docs/))
- `make`

### Setup poetry

Install dependencies and check the environment is set up correctly:

```bash
$ make install
$ make test
$ make lint
```

### Launch a development server

The development server uses [uvicorn](https://www.uvicorn.org/) and [FastAPI](https://fastapi.tiangolo.com/). You can launch the development server with the `uvicorn` CLI.

```bash
# Using uvicorn
$ make run

# Using Python directly (adds watcher)
$ make run-py
```

You can run the tests with `pytest` via `make test`.

### Create your own docker image and run it

Build application package:

```sh
make install
```

Build Docker image:

```sh
# using the makefile (recommended)
make docker-build

# manual build (requires to set version)
docker build --build-arg VERSION=`poetry version -s` .
```

Run Docker image:

```sh
docker run -p 5000:5000/tcp boavizta/boaviztapi:`poetry version -s`
```

#### Alternative (if you don't have Python or Poetry)

```sh
make docker-build-development

make docker-run-development
```

### Deploy to AWS as serverless application

You can self-host BoaviztAPI as an AWS Lambda function using [Serverless Framework](https://www.serverless.com/framework).

You must first configure:

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
- [Serverless Framework CLI](https://www.serverless.com/framework/docs/getting-started)

Once done, you can deploy the API with:

```sh
serverless deploy
```

When the deploy succeeds, it will show you the URLs for the deployed function, and you can call the API as normal, e.g.

```sh
# Replace the base URL with your own
curl -s "https://k9wllbzcc2.execute-api.eu-west-1.amazonaws.com/v1/server/?archetype=dellR740"
```

You can check your Lambda URL at any time with:

```sh
serverless info
```

### OpenAPI specification (Swagger)

Once API server is launched API swagger is available at [httsp://localhost:5000/docs](https://localhost:5000/docs).

## :woman: Contributing

See [contributing.md](./CONTRIBUTING.md).

You can build a source distribution (installable with pip) with `make build`.

## :one: Versioning

We use [Semantic Versioning 2.0.0](https://semver.org/)

|    Type     | Description                                                          |    Command        |
| :---        |    :----:                                                            |              ---: |
| MAJOR       | version when you make incompatible API changes                       | ```make major```  |
| MINOR       | version when you add functionality in a backwards compatible manner  | ```make minor```  |
| PATCH       | version when you make backwards compatible bug fixes                 | ```make patch```  |

## :two: Releasing

See the [Release Process wiki](https://github.com/Boavizta/boaviztapi/wiki/Release-Process).

## :scroll: License

GNU Affero General Public License v3.0
