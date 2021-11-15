# Tools-API

Giving access to BOAVIZTA referenced datas and methodologies trought a RESTful API

## Objective

As part of Boavizta's desire to improve the quality of the measurement of the environmental impacts of ICTs in organizations, this project aims to give access to the group's work to as many people as possible in an automated and industrialized way.  

The various data and methodologies integrated by Boavizta are aggregated and made available via an API. 

In the interest of transparency and scientific popularization, the opening of the code, the versioning of the impact factors and the documentation of the project are critical points. 

## Architecture

The system is developed in layers according to a bottom-up principle. The first layer implemented is equipment, starting with the servers (MVP). The second layer is the measurement of the impact of digital services or systems. The measurement of the global impact is currently outside the scope. 

## Technos

* Flask 2.0.2
* Python >= 3.6

## Coding convention

[PEP8](https://www.python.org/dev/peps/pep-0008/)
