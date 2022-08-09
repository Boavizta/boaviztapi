<p align="center">
    <img src="https://raw.githubusercontent.com/Boavizta/boaviztapi/dev/boavizta-logo-4.png" width="100">
</p>
<h1 align="center">
  Boavizta API
</h1>

---

An API to access [Boavizta's](https://boavizta.cmakers.io/) methodologies and footprint [reference data](https://github.com/Boavizta/environmental-footprint-data).

See the [documentation](https://doc.api.boavizta.org/) for API usage and methodology.

[![Python tests main](https://github.com/Boavizta/Tools-API/actions/workflows/main-main.yml/badge.svg)](https://github.com/Boavizta/Tools-API/actions/workflows/main-main.yml)

## :dart: Objective

As part of Boavizta's desire to improve the quality of the measurement of the environmental impacts of ICTs in organizations, this project aims at giving access to the group's work to as many people as possible in an automated and industrialized way.

The various data and methodologies integrated by Boavizta are aggregated and made available via an API.

In the interest of transparency and scientific popularization, the opening of the code, the versioning of the impact factors and the documentation of the project are critical points.

The system is developed in layers according to a bottom-up principle. The first layer implemented is equipment, starting with the servers (MVP). The second layer is the measurement of the impact of digital services or systems. The measurement of the global impact is currently outside the scope.

## :fast_forward: Test it yourself (no installation)

* See the OpenAPI specification: <https://api.boavizta.org/docs>

* [Documentation](https://doc.api.boavizta.org/)

* Access the demo API: <https://api.boavizta.org>

## Run a local instance

## :whale: Run API using docker

```bash
$ docker run ghcr.io/boavizta/boaviztapi:latest
```

## 📦 Install using pip package

```bash
$ pip3 install boaviztapi
```


## :computer: Development

### Prerequisite

Python 3, pipenv recommended

### Setup pipenv

Install pipenv globally

```bash
$ sudo pip3 install pipenv
```

Install dependencies and create a python virtual environment.

```bash
$ pipenv install -d
$ pipenv shell
```

### Launch a development server

**Once in the pipenv environment**

Development server uses [uvicorn](https://www.uvicorn.org/) and [fastapi](https://fastapi.tiangolo.com/), you can launch development server with the `uvicorn` CLI.

```bash
$ uvicorn boaviztapi.main:app --host=localhost --port 5000
```

You can run the tests with `pytest`.

### OpenAPI specification (Swagger)

Once API server is launched API swagger is available at [httsp://localhost:5000/docs](https://localhost:5000/docs).


## :woman: Contributing

See [contributing.md](./CONTRIBUTING.md)

You can build a source distribution (installable with pip) with `python setup.py sdist`.

## :one: Versioning

We use [Semantic Versioning 2.0.0](https://semver.org/)

|    Type     | Description                                                          |    Command        |
| :---        |    :----:                                                            |              ---: |
| MAJOR       | version when you make incompatible API changes                       | ```make major```  |
| MINOR       | version when you add functionality in a backwards compatible manner  | ```make minor```  |
| PATCH       | version when you make backwards compatible bug fixes                 | ```make patch```  |

## :scroll: License

GNU Affero General Public License v3.0
