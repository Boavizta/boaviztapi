# Tools-API

Giving access to BOAVIZTA referenced datas and methodologies trought a RESTful API

## Objective

As part of Boavizta's desire to improve the quality of the measurement of the environmental impacts of ICTs in organizations, this project aims at giving access to the group's work to as many people as possible in an automated and industrialized way.  

The various data and methodologies integrated by Boavizta are aggregated and made available via an API. 

In the interest of transparency and scientific popularization, the opening of the code, the versioning of the impact factors and the documentation of the project are critical points. 

## Architecture

The system is developed in micro-services layers according to a bottom-up principle. The first layer implemented is equipment, starting with the servers (MVP). The second layer is the measurement of the impact of digital services or systems. The measurement of the global impact is currently outside the scope. 

## Installation

Create a virtual environment and activate it.

```bash
python3 -m venv venv
source venv/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install project requirements.

```bash
pip install -r requirements.txt
```

## Usage

### Launch development API server

Development server uses [uvicorn](https://www.uvicorn.org/) and [fastapi](https://fastapi.tiangolo.com/), you can launch either with a python script or with the `uvicorn` CLI.

```bash
python3 main.py
```

OR

```bash
uvicorn main:app --host=localhost --port 5000
```

### API Swagger

Once API server is launched API swagger is available at [http://localhost:5000/docs](http://localhost:5000/docs).

### Launch using docker container
```bash
docker run ghcr.io/boavizta/tools-api:latest
```

## Contributing

TODO

## License

TODO
