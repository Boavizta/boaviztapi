# Deploy the API

## Docker

```bash
$ docker run -p 5000:5000 ghcr.io/boavizta/boaviztapi:latest
```

Exposes the API at <http://localhost:5000>.

## Docker Compose

```bash
# Using Docker images from GCR
docker compose -f compose-prod.yaml up

# Building images from source
docker compose up
```

Exposes the API at <http://localhost:5000>, and the docs at <http://localhost:8080>.

## AWS Lambda

### Prerequisites

- [AWS](https://aws.amazon.com/) and [Serverless Framework](https://www.serverless.com/) accounts
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
- [Serverless Framework CLI](https://www.serverless.com/framework/docs/getting-started)

### Deployment

```sh
serverless deploy
```

When the deploy succeeds, it will show you the URLs for the deployed function, and you can call the API as normal. You can query these URLs at any time with `serverless info`.

## From source

### Prerequisites

- Python >=3.12
- [Poetry](https://python-poetry.org/)
- `make`

### Clone the repo

```bash
$ git clone https://github.com/Boavizta/boaviztapi.git
```

### Install

```bash
$ make install
```

### Launch the server

```bash
$ make run
```

## SDK

You can also use BoaviztaAPI directly in code with the SDKs:

- **python-sdk** : [https://pypi.org/project/boaviztapi-sdk/](https://pypi.org/project/boaviztapi-sdk/)
- **rust-sdk** : [https://github.com/Boavizta/boaviztapi-sdk-rust](https://github.com/Boavizta/boaviztapi-sdk-rust)
