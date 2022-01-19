# BOAVIZTAPI [![Python tests main](https://github.com/Boavizta/Tools-API/actions/workflows/main-main.yml/badge.svg?branch=main)](https://github.com/Boavizta/Tools-API/actions/workflows/main-main.yml)

Giving access to BOAVIZTA referenced datas and methodologies trought a RESTful API

## Objective

As part of Boavizta's desire to improve the quality of the measurement of the environmental impacts of ICTs in organizations, this project aims at giving access to the group's work to as many people as possible in an automated and industrialized way.  

The various data and methodologies integrated by Boavizta are aggregated and made available via an API. 

In the interest of transparency and scientific popularization, the opening of the code, the versioning of the impact factors and the documentation of the project are critical points.

The system is developed in layers according to a bottom-up principle. The first layer implemented is equipment, starting with the servers (MVP). The second layer is the measurement of the impact of digital services or systems. The measurement of the global impact is currently outside the scope. 

## Test it yourself

* Test the API : TODO

* Dev documentation server : http://149.202.185.115/

* Dev API server: http://149.202.185.115:5000

## Setup project locally with pipenv

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

### API Swagger

Once API server is launched API swagger is available at [http://localhost:5000/docs](http://localhost:5000/docs).

## Install using docker container
```bash
$ docker run ghcr.io/boavizta/boaviztapi:latest
```

## Install using pip package
```bash
$ pip3 install boaviztapi
```

## Contributing

See [contributing.md](./CONTRIBUTING.md)

You can build a source distribution (installable with pip) with `python setup.py sdist`.

## Versionning

We use [Semantic Versioning 2.0.0](https://semver.org/)

|    Type     | Description                                                          |    Command        |
| :---        |    :----:                                                            |              ---: |
| MAJOR       | version when you make incompatible API changes                       | ```make major```  |
| MINOR       | version when you add functionality in a backwards compatible manner  | ```make minor```  |
| PATCH       | version when you make backwards compatible bug fixes                 | ```make patch```  |

## License

TODO
