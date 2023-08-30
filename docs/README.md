# Documentation

Documentation of Boaviztapi

Content:

1. ADR - Architecture decision records
2. assets: static content like images
3. Explanations: Functional documentation - Equations & key concepts are explained
4. DEMO - an executable openAPI spec (former swagger)
5. Getting started: some basic API queries explained.
6. How to guides - for developers who want to use the API

## Install & launch a local documentation server

Documentation is generated from markdown using `mkdocs` with the `material` theme.

```bash
# install mkdocs and its extensions
pip install mkdocs mkdocs-render-swagger-plugin mkdocs-material mkdocs-macros-plugin
```

💡 Do not mixup _pip_ and _brew_ installation of `mkdocs` (see [troubleshooting](https://jimandreas.github.io/mkdocs-material/troubleshooting/)).

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
