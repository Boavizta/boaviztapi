# Adopters

This page lists projects and organizations that use BoaviztAPI.

## [Boavizta](https://boavizta.org)

### [Datavizta](https://datavizta.boavizta.org)

The official interactive front-end for BoaviztAPI. Datavizta provides a web dashboard for exploring and visualizing the environmental impacts of servers, cloud instances, and end-user devices. It is a direct consumer of the BoaviztAPI REST endpoints (`/v1/server`, `/v1/cloud/instance`, etc.).

### [CloudScanner](https://github.com/Boavizta/cloud-scanner)

A CLI tool and service that scans an AWS account, inventories running EC2 instances, and returns real-time environmental impact estimates (GWP, ADP, PE). CloudScanner calls BoaviztAPI's `/v1/cloud/instance` endpoint, passing instance type and usage data to retrieve per-instance impact figures.

### [Boagent](https://github.com/Boaviztapi/boagent)

A monitoring agent modeling the environmental footprint of the local machine it is installed on. This is done by:
1. Scanning the hardware visible on the machine, producing a Bill Of Material
2. Collecting power usage metrics from Scaphandre
3. Asking BoaviztAPI to compute the full lifecycle environmental footprint of the machine and its usage.

## [EcoLogits](https://ecologits.ai)

A Python library that tracks the energy consumption and environmental impacts of generative AI inference across major LLM API providers (OpenAI, Anthropic, Mistral, etc.). EcoLogits uses BoaviztAPI as its underlying methodology engine to compute the embedded (manufacturing) and use-phase (electricity) environmental impacts of the GPU servers running LLM inference. See the [LLM inference methodology](https://ecologits.ai/latest/methodology/llm_inference/) for details.

## [G4IT](https://saas-g4it.com/documentation)

An open-source and mutualized platform for evaluate impact of information system and digital services, which permit to deploy at a large scale environmental assessment of IT.

## [Scaleway](https://www.scaleway.com/)

Scaleway use the BoaviztAPI for their [environmental footprint calculator](https://www.scaleway.com/en/docs/environmental-footprint/additional-content/environmental-footprint-calculator/).

## [SPRUCE](https://github.com/DigitalPebble/spruce)

An [open-source enrichment platform for GreenOps](https://opensourcegreenops.cloud/) which helps measure and reduce the environmental impact of cloud computing. SPRUCE uses BoaviztAPI to retrieve hardware impact data for the servers powering cloud workloads.

## [Carenage](https://gitlab.com/hubblo/carenage)

Carenage is a continuous integration tool meant to make environmental evaluation easier for software projects. Used in CI scripts, it queries needed metrics and metadata during the execution of a CI job to insert them into a database. Afterwards, the data is available as JSON objects through requests to a RESTful API and visualisable in a dashboard.
