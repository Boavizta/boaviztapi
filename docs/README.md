# Documentation

Documentation of Boavizta tools-API.

Contains:

1) ADR - Architecture decision records
2) DEMO - Via swagger
3) Functional documentation - Equations & key concepts are explained
4) How to guide - for developers who want to use the API

## Install & launch a local documentation server

```bash
pip install mkdocs mkdocs-render-swagger-plugin
```

```bash
# from the root of the cloned repository
cd docs
mkdocs serve
```

Open <http://localhost:8080>

## Access latest published documentation using docker

```bash
docker run ghcr.io/boavizta/tools-doc:latest
```
