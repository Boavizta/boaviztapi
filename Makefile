CURRENT_VERSION := $(shell poetry version -s || sed -n '3s/.*version = "\(.*\)"/\1/p' pyproject.toml)
TIMESTAMP := $(shell date "+%H.%M-%m-%d-%y")
DOCKER_NAME := boavizta/boaviztapi:${CURRENT_VERSION}
SEMVERS := major minor patch

MINIMUM_PY_VERSION=3.8
MAXIMUM_PY_VERSION=3.11

clean:
		find . -name "*.pyc" -exec rm -rf {} \;
		rm -rf dist *.egg-info __pycache__

install: install_pip

install_pip:
		poetry install --with dev

test:
		poetry run pytest

define compat-check
		docker build -t boavizta/boaviztapi-py$(1) \
			--target build-env \
			--build-arg VERSION=0.0.1 \
			--build-arg PY_VERSION=$(1) \
			.
		docker run \
			-v $(shell pwd):/app \
 			boavizta/boaviztapi-py$(1) \
			poetry run pytest
endef

test-compat-min:
	$(call compat-check,${MINIMUM_PY_VERSION})

test-compat-max:
	$(call compat-check,${MAXIMUM_PY_VERSION})

run:
		poetry run uvicorn boaviztapi.main:app

$(SEMVERS):
		poetry version $@
		$(MAKE) npm_version
		$(MAKE) tag_version

npm_version:
		npm version --no-git-tag-version ${CURRENT_VERSION}


tag_version:
		git commit -m "release: bump to ${CURRENT_VERSION}" pyproject.toml package.json package-lock.json
		git tag ${CURRENT_VERSION}

build:
		poetry build

distribute:
		poetry config pypi-token.pypi ${API_TOKEN}
		poetry publish --build

docker-build:
		docker build -t $(DOCKER_NAME) .  --build-arg VERSION=${CURRENT_VERSION}

docker-build-development:
		docker build -t boavizta/boaviztapi:${TIMESTAMP} .  --build-arg VERSION=${TIMESTAMP}
