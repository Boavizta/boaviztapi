# Deploy the API

## Deploy

### with docker

```bash
$ docker run  -p 5000:5000 ghcr.io/boavizta/boaviztapi:1.0.0a4
```

Then access api at <http://localhost:5000>

### with docker-compose

```yaml
version: "3.9"
services:
  boaviztapi:
    image: ghcr.io/boavizta/boaviztapi:1.0.0a4
    environment:
      - SPECIAL_MESSAGE="<p>my welcome message in HTML format</p>"
    ports:
      - "5000:5000"
  boaviztapi-doc:
    image: ghcr.io/boavizta/boaviztapi-doc:latest
    environment:
      - API_URL=http://boaviztapi_url.com
    ports:
      - "8080:8080"
```

### with pip

boaviztapi pip package : [https://pypi.org/project/boaviztapi/](https://pypi.org/project/boaviztapi/)

```bash
$ pip3 install boaviztapi
```

### from source

#### Prerequisite

Python 3, pipenv recommended

#### clone the repo

```bash
$ git clone https://github.com/Boavizta/boaviztapi.git
```

#### Setup pipenv

Install pipenv globally

```bash
$ sudo pip3 install pipenv
```

Install dependencies and create a python virtual environment.

```bash
$ pipenv install -d 
$ pipenv shell
```

#### Launch a development server

Once in the pipenv environment

Development server uses [uvicorn](https://www.uvicorn.org/) and [fastapi](https://fastapi.tiangolo.com/), you can launch development server with the `uvicorn` CLI.

```bash
$ uvicorn boaviztapi.main:app --host=localhost --port 5000
```

### CORS

By default, all origin are allowed. If you need to limit them set env value ```ALLOWED_ORIGINS``` with the following format : ```ALLOWED_ORIGINS = '["url1", "url2", ...]'```

Example : ```ALLOWED_ORIGINS='["https://datavizta.boavizta.org","https://boavizta.org"]'```

### Special message

You can customize the home page with a special message by setting the env value ```SPECIAL_MESSAGE`` in HTML format.

Example : ```SPECIAL_MESSAGE="<p>my welcome message in HTML format</p>"```


## SDK

**python-sdk** : [https://pypi.org/project/boaviztapi-sdk/](https://pypi.org/project/boaviztapi-sdk/)

**rust-sdk** : [https://github.com/Boavizta/boaviztapi-sdk-rust](https://github.com/Boavizta/boaviztapi-sdk-rust)