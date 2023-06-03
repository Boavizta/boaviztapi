CURRENT_VERSION := $(shell poetry version -s)
DOCKER_NAME := boavizta/boaviztapi:${CURRENT_VERSION}

clean:
		find . -name "*.pyc" -exec rm -rf {} \;
		rm -rf dist *.egg-info __pycache__

install: install_pip

install_pip:
		poetry install --with dev

test:
		poetry run pytest

run:
		poetry run uvicorn boaviztapi.main:app

minor:
		poetry run bumpversion --commit --tag --current-version ${CURRENT_VERSION} minor boaviztapi/__init__.py

major:
		poetry run bumpversion --commit --tag --current-version ${CURRENT_VERSION} major boaviztapi/__init__.py

patch:
		poetry run bumpversion --commit --tag --current-version ${CURRENT_VERSION} patch boaviztapi/__init__.py

build:
		poetry build

distribute:
		poetry config pypi-token.pypi ${API_TOKEN}
		poetry publish --build

docker-build:
		docker build -t $(DOCKER_NAME) .

